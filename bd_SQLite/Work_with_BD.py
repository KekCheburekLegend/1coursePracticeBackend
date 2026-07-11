import os
import sqlite3
import encode



def Connnect_DB():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(current_dir, 'Short_link_BD')
    connect = sqlite3.connect(db_path)
    
    return connect


def Path_new_url(Url:encode.URLRequest) -> str:
    connect = Connnect_DB()
    cursor = connect.cursor()
    cursor.execute('Select ShortUrl from Url Where LongUrl = ?', (str(Url.url), ))
    res_find = cursor.fetchone()
    if res_find is not None:
        return res_find[0]
    else:
        cursor.execute('SELECT MAX(id) FROM Url')
        result = cursor.fetchone()
        current_max_id = result[0] if result[0] is not None else 0
        next_id = current_max_id + 1
        short_code = encode.encode_url(next_id)
        
        original_url = Url.url 
        cursor.execute(
            'INSERT INTO Url (id, LongURL, ShortURL) VALUES (?, ?, ?)',
            (next_id, str(original_url), short_code)
        )
        connect.commit()

    connect.close()
    return short_code


def Try_find_short(short:str):
    connect = Connnect_DB()
    cursor = connect.cursor()
    cursor.execute('select LongUrl from Url where ShortUrl = ?', (short, ))
    link = cursor.fetchone()
    connect.close()
    if link is not None: 
        return link[0]
    return None




    


