import sqlite3 as lite
def get_row_for_id(id,table):
    con = lite.connect('Tableau.db')
    cursor = con.cursor()
    cursor.execute('''FROM table=? WHERE id=?''',(table,id))
    row = cursor.fetchone()
    return row
    con.commit()
            
        
