import mysql.connector

try:
    conn = mysql.connector.connect(
        host="127.0.0.1",
        port=3306,
        user="root",
        password="16.13@Ka",   # ✅ your real password
        database="mst_db",
        auth_plugin='mysql_native_password'  # ✅ critical fix
    )

    if conn.is_connected():
        print("✅ Connection Successful to MySQL Workbench!")

except mysql.connector.Error as err:
    print("❌ Connection Failed:", err)

finally:
    if 'conn' in locals() and conn.is_connected():
        conn.close()
