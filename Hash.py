U
    þ^�7  �                	   @   s<  d dl Z d dlZd dlZd dlZd dlZd dlZd dlmZ d dlmZ dddddd	d
dd�Z	G dd� d�Z
G dd� de
�Zedk�r8e�� Ze�� Ze�� Zd#dd�Zdd� Zdd� Zdd� Ze�d� ed� zeed��ZW n   e�d� Y nX edk�re�  n,ed k�re�  ned!k�r0e�  ned"� dS )$�    N)�Fernet)�datetimezSHA1()zSHA224()zSHA256()zSHA384()zSHA512()z	BLAKE2b()z	BLAKE2s()zMD5())�   �   �   �   �   �   �   �   c                   @   s   e Zd Zdd� Zdd� ZdS )�
CryptoHashc                 C   s�   |� � }| dkr"t�|��� }|S | dkr<t�|��� }|S | dkrVt�|��� }|S | dkrpt�|��� }|S | dkr�t�|��� }|S | dkr�t�|��� }|S | dkr�t�	|��� }|S | dkr�t�
|��� }|S td	� d S )
Nr   r   r   r   r   r	   r
   r   zInvalid Code!)�encode�hashlib�sha1�	hexdigestZsha224Zsha256Zsha384�sha512�blake2b�blake2s�md5�print)�code�txt�text�Hash� r   �(/data/data/com.termux/files/home/Hash.pyr      s4    zCryptoHash.Hashc                 C   s�   | � � }t�|��� � � }t�|��� }t�dd�t�dd� }}|d |� � � ||d � � �  }}t�|��� }t�|��� }	||	 � � }
t�	|
��� }t
�� }t
|�}|�|�}|||d�S )Nr   �   �    )r   �File�Key)r   r   r   r   r   �random�randintr   r   r   r   Zgenerate_keyZencrypt)r   r   ZHashBbZHashBsZran_1Zran_2Zsplit_1Zsplit_2ZHashS1ZHashS512Z	HashMergeZHashMd5r   �FerZEncryptr   r   r   �KeyHash6   s    "
zCryptoHash.KeyHashN)�__name__�
__module__�__qualname__r   r#   r   r   r   r   r      s   r   c                   @   s:   e Zd Zdd� Zddd�Zddd�Zddd	�Zd
d� ZdS )�DataBasec                  C   sB   t j�d�rt�d�S t�d�} | �d� | �d� t�d�S d S )N�HashData.db�CCREATE TABLE Hashes(Hash Text Not Null Unique, Value Text Not Null)�QCREATE TABLE KeyHashes(KeyId Int Not Null,Hash Text Not Null,Value Text Not Null)��os�path�exists�sqlite3�connect�execute��connr   r   r   �
ConnectionO   s    



zDataBase.Connection� c           
      C   s�   t �� }|dkr�tj�|�r�t|d�}|�� }zB|�d�| ��}|D ]}|d �	� }qDt
|�}|�|�}	|	�� W S    t�d� Y q�X q�t�d� n@z(|�d�| ��}|D ]}|d }q�|W S    t�d� Y nX d S )	Nr5   Zrbz-SELECT Value FROM KeyHashes WHERE Hash ='{0}'r   u   【!】Key Or Hash Not Matchu   【!】Key Not Foundz+SELECT Value FROM Hashes WHERE Hash = '{0}'�   【!】Hash Not Found)r'   r4   r,   r-   r.   �open�readr1   �formatr   r   Zdecrypt�decode�sys�exit)
r   r   r3   ZkeyFileZmainKey�ret�i�valr"   Ztokenr   r   r   �RetrieveZ   s,    



zDataBase.Retrievec                 C   s~   t �� }|dkrNt�dd�}z |�d�|| |�� |��  W n   Y nX |S z|�d�| |�� |��  W n   Y nX d S )Nr5   i�  i���z-INSERT INTO KeyHashes VALUES({0},'{1}','{2}')z&INSERT INTO Hashes VALUES('{0}','{1}'))r'   r4   r    r!   r1   r9   �commit)r   �Textr   r3   ZgenIdr   r   r   �Insertu   s    zDataBase.Insertc           
      C   sx  dd� }t �� }|dkr�|� }| dkrl|dkrl|�d�}|D ]*}|\}}}	|�d�|||	�� |��  q<dS zH|�d�| |��}|D ]*}|\}}}	|�d�|||	�� |��  q�W dS    t�d	� Y nX n�|� }| dk�r|�d
�}|D ]&}|\}}	|�d�||	�� |��  q�dS zD|�d�| ��}|D ](}|\}}	|�d�||	�� |��  �q.W dS    t�d� Y nX d S )Nc                  S   sB   t j�d�rt�d�S t�d�} | �d� | �d� t�d�S d S )N�ShareData.dbz<CREATE TABLE Hashes(Hash Text Not Null, Value Text Not Null)r*   r+   r2   r   r   r   �Sdb�   s    



zDataBase.ShareHash.<locals>.Sdbr5   �*zSELECT * From KeyHashes�-INSERT INTO KeyHashes Values({0},'{1}','{2}')Tz5SELECT * FROM KeyHashes WHERE Hash='{0}'AND KeyId={1}u   【!】KeyId And Hash Not FoundzSELECT * From Hashes�&INSERT INTO Hashes Values('{0}','{1}')z%SELECT * FROM Hashes WHERE Hash='{0}'r6   )r'   r4   r1   r9   rA   r;   r<   )
r   �KeyIdrE   r3   ZsDb�datar>   �Id�H�Vr   r   r   �	ShareHash�   sJ    	







zDataBase.ShareHashc                 C   s�   t j�| �r�t�| �}t j�d�r.t�d�}nt�d�}|�d� |�d� |�d�}|�d�}|D ]8}|\}}z|�d�||�� |��  W qd   Y qdX qd|D ]*}|\}	}
}|�d�|	|
|�� |��  q�dS t�	d	� d S )
Nr(   r)   r*   zSELECT * FROM HasheszSELECT * FROM KeyHashesrH   rG   T�   【!】DataBase Not Found)
r,   r-   r.   r/   r0   r1   r9   rA   r;   r<   )ZdbZconn2r3   Zdata1Zdata2r>   ZH1ZV1�jrK   ZH2ZV2r   r   r   �JoinDb�   s,    







zDataBase.JoinDbN)r5   )r5   r5   )r5   )r$   r%   r&   r4   r@   rC   rN   rQ   r   r   r   r   r'   L   s
   


5r'   �__main__r5   c                 C   s�   t j�d�rt �d� nt �d� t �d� |dkr�|dkr�tdd�}|�d�tt	| |�� |�
�  |�� }t|d d�}|�|� |�
�  n&tdd�}|�d	�tt	| �� |�
�  d S )
Nr   r5   �KeyHash.txt�az3
Date : {0}
Time : {1}
KeyHash : {2}
KeyId : {3}


z.key�wbzHash.txtz$
Date : {0}
Time : {1}
Hash : {2}


)r,   r-   r.   �chdir�mkdirr7   �writer9   �realDate�realTime�closer   )r   rI   r   �f�kr   r   r   �file�   s8    


   ��


  ��r^   c                  C   s:  t �d� td� td� �zttd��} | tdd�k�rtd�}|dk�r
| dkr�t�|�}td	� t�	d
� td|d  � t
j|d |d �� d�}t|�}td| � t|d ||d �� � n@t�| |�}td	� t�	d
� td| � t
j||d� t|� ntd� ntd� W n   t�d� Y nX d S )N�clear�   		【SecuredHash】
u|   【1】SHA1	【2】SHA224	【3】SHA256
【4】SHA384	【5】SHA512	【6】BLAKE2b
【7】BLAKE2s	【8】MD5	【0】KeyHash
u   【➜】Enter Code : r   �	   u   【➜】Enter Text : r5   u   【☢】Generating Hash...g      �?u   【☻】KeyHash : r   r   )r   �   【$】KeyId : r   u   【☻】Hash : )rB   u   【!】Please Enter Somethingu   【!】Invalid Code!zSomething Wrong!)r,   �systemr   �int�input�ranger   r#   �time�sleepr'   rC   r:   �strr^   r   r;   r<   )r   r   r   rK   ZkeyIdr   r   r   �Crypt  s6    






rj   c                  C   s�  t �d� td� zttd��} td�}W n   t�d� Y nX | dkrvtd� t�d� t	�
|�}td	| � �n<| dkr�ztd
�}W n   t�d� Y nX td� t�d� t	�
||�}td	| � n�| dk�r�t j�d��r�t�d�}z8td�}td� t�d� |�d�||�� |��  W n   t�d� Y nX t j�d��rZt �d� nt �d� t �d� tdd�}|�d�tt||�� |��  td� ntd� ntd� d S )Nr_   u<   		【DeHash】

【1】Hash	【2】KeyHash	【3】RmKeyHash
u   【➜】Choose : �   【➜】Past Your Hash : �   【!】Something Wrongr   u   【☯】Searching...r   u   【✔】DeHash : u   【฿】Key : r   r(   rb   u   【☯】Removing...z3DELETE FROM KeyHashes WHERE Hash='{0}'AND KeyId={1}r   rS   rT   uR   
                【!】Removed
Date : {0}
Time : {1}
KeyHash : {2}
KeyId : {3}


u   【✔】KeyHash RemovedrO   �   【!】Invalid Number)r,   rc   r   rd   re   r;   r<   rg   rh   r'   r@   r-   r.   r/   r0   r1   r9   rA   rV   rW   r7   rX   rY   rZ   r[   )ZhashType�hr?   r]   r3   r\   r   r   r   �DeHash,  sb    









   ��	

ro   c                  C   s*  t �d� td� ztd�} W n   t�d� Y nX | dkr�t j�d�r�td� t�	d� ztd	�}td
�}W n   t�d� Y nX |dkr�td� t�	d� t
�||� td� q�td� ntd� nZ| dk�rt j�d��rt
�d� td� t �d� t�	d� td� ntd� ntd� d S )Nr_   u   		【ShareHash】
u3   【1】ShareData【2】MergeData
【➜】Choose : rl   �1r(   u�   
【☻】If You Want To Share KeyHash Data So Give KeyId OtherWise Leave Blank!
【☻】If You Want To Select All Hash So Type In Hash Field 【*】. 
【☻】If You Want To Select All KeyHash So Type In Both Field【*】.
r   rk   rb   r5   u   【☢】Creating DataBase...u   【✔】ShareData.db Createdu!   【!】Read Instructions Properlyu   【!】HashData.db Not Found�2rD   u   【☯】Merging Data...u   【✔】Data Mergedu   【!】ShareData.db Not Foundrm   )r,   rc   r   re   r;   r<   r-   r.   rg   rh   r'   rN   rQ   �remove)ZsHr   rI   r   r   r   �sHashc  s>    











rs   r_   r`   u=   【1】Hash	【2】DeHash	【3】ShareHash
【➜】Choose : rl   r   r   r   rm   )r5   r5   )r   r,   r    r;   r/   rg   Zcryptography.fernetr   r   Z	hashCodesr   r'   r$   Znow�drZ   �daterY   r^   rj   ro   rs   rc   r   rd   re   Zchor<   r   r   r   r   �<module>   sF   0�7 

$%7&



