import mysql.connector

db_config = {
    'user': 'jh2dvz9avl3a72p1730j',
    'password': 'pscale_pw_iFA7hl6fX6GQCw7V9bf64POx4gbUGQfJCNCGpaeFBO4',
    'host': 'aws.connect.psdb.cloud',
    'database': 'content_database'
}

def save_subbed_feed_info(email, subbed_feed):
  try:
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    select_query = "SELECT * FROM user_info WHERE Email = %s"
    cursor.execute(select_query, (email,))
    result = cursor.fetchone()
    print(result)

    if result:
      # Email already exists, append Subbed_Feed to the previous value
      previous_subbed_feed = result[3]  # Index 3 represents the Subbed_Feed column
      print(previous_subbed_feed)
      if previous_subbed_feed is None:
        new_subbed_feed = subbed_feed
      else:
        new_subbed_feed = f"{previous_subbed_feed},{subbed_feed}"
      print(new_subbed_feed)

      update_query = "UPDATE user_info SET Subbed_Feeds = %s WHERE Email = %s"
      cursor.execute(update_query, (new_subbed_feed, email))
    else:
      # Email does not exist, create a new row
      insert_query = "INSERT INTO user_info (Email, Subbed_Feeds) VALUES (%s, %s)"
      data = (email, subbed_feed)
      cursor.execute(insert_query, data)

    conn.commit()

    cursor.close()
    conn.close()

    return True
  except mysql.connector.Error as error:
    print("Error while connecting to MySQL:", error)
    return False


# def save_user_info(Email, Subbed_Feed):
#   try:
#     conn = mysql.connector.connect(**db_config)
#     cursor = conn.cursor()

#     insert_query = "INSERT INTO test_user_info (Email, Subbed_Feed) VALUES (%s, %s)"
#     print('into datbase')
#     data = (Email, Subbed_Feed)
#     cursor.execute(insert_query, data)
#     conn.commit()

#     cursor.close()
#     conn.close()

#     return True
#   except mysql.connector.Error as error:
#     print("Error while connecting to MySQL:", error)
#     return False

def select_query(query, param1):
  try:
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    select_query = "SELECT * FROM test_user_info WHERE Email = %s"
    cursor.execute(select_query, (email,))
    result = cursor.fetchone()
    print(result)

    if result:
      # Email already exists, append Subbed_Feed to the previous value
      previous_subbed_feed = result[3]  # Index 3 represents the Subbed_Feed column
      new_subbed_feed = f"{previous_subbed_feed},{subbed_feed}"
      print(new_subbed_feed)

      update_query = "UPDATE test_user_info SET Subbed_Feed = %s WHERE Email = %s"
      cursor.execute(update_query, (new_subbed_feed, email))
    else:
      # Email does not exist, create a new row
      insert_query = "INSERT INTO test_user_info (Email, Subbed_Feed) VALUES (%s, %s)"
      data = (email, subbed_feed)
      cursor.execute(insert_query, data)

    conn.commit()

    cursor.close()
    conn.close()

    return True
  except mysql.connector.Error as error:
    print("Error while connecting to MySQL:", error)
    return False

def if_email_exists(email):
  try:
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    select_query = "SELECT email FROM user_info WHERE email = %s"
    cursor.execute(select_query, (email,))
    result = cursor.fetchone()

    conn.commit()
    cursor.close()
    conn.close()

    if result:
        return True
    else:
        return False
  except mysql.connector.Error as error:
    print("Error while connecting to MySQL:", error)
    return False

def if_password_matches(email, password):
  try:
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    select_query = "SELECT email FROM user_info WHERE email = %s AND pass = %s"
    cursor.execute(select_query, (email, password))
    result = cursor.fetchone()

    conn.commit()
    cursor.close()
    conn.close()

    if result:
        return True
    else:
        return False
  except mysql.connector.Error as error:
    print("Error while connecting to MySQL:", error)
    return False


def save_user_info(email, password):
  try:
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    insert_query = "INSERT INTO user_info (email, `pass`) VALUES (%s, %s)"
    data = (email, password)
    cursor.execute(insert_query, data)

    conn.commit()
    cursor.close()
    conn.close()

    return True
  except mysql.connector.Error as error:
    print("Error while connecting to MySQL:", error)
    return False

def get_subbed_feeds(email):
  try:
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    select_query = "SELECT subbed_feeds FROM user_info WHERE email = %s"
    cursor.execute(select_query, (email,))
    result = cursor.fetchone()
    print(result)

    if result:
      subbed_feed = result[0]  # Retrieve the subbed_feed value
      print(subbed_feed)
      if subbed_feed is None:
        return []
      subbed_feed_list = subbed_feed.split(',')  # Split the subbed_feed by comma
      return subbed_feed_list
    else:
      return []

  except mysql.connector.Error as error:
    print("Error while connecting to MySQL:", error)
    return []

  finally:
    cursor.close()
    conn.close()


def fetch_articles_by_domains(domains):
  try:
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    articles = []

    for domain in domains:
      # Construct the query to fetch articles with the current domain
      query = "SELECT title, link, summary, pubDate FROM feed_info WHERE link LIKE %s ORDER BY pubDate DESC"

      # Execute the query with the current domain
      cursor.execute(query, ('%' + domain + '%',))

      # Fetch all the articles for the current domain
      for row in cursor.fetchall():
        title, link, summary, pubDate = row
        articles.append({'title': title, 'link': link, 'description': summary, 'pubDate': pubDate})

    return articles

  except mysql.connector.Error as e:
    # Handle the database error
    print("Database error:", e)
    return []

  finally:
    # Close the cursor and connection
    cursor.close()
    conn.close()
