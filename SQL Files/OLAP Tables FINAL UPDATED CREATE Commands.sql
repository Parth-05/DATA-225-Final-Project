CREATE TABLE Menu_Dim
(
  menu_id INT NOT NULL,
  category VARCHAR(100) NOT NULL,
  item_name VARCHAR(100) NOT NULL,
  price FLOAT NOT NULL,
  rating FLOAT NOT NULL,
  PRIMARY KEY (menu_id)
);

CREATE TABLE Date_Dim
(
  day INT NOT NULL,
  month INT NOT NULL,
  year INT NOT NULL,
  dow INT NOT NULL,
  PRIMARY KEY (day, month, year)
);

CREATE TABLE User_Dim
(
  user_id INT NOT NULL,
  name VARCHAR(100) NOT NULL,
  email VARCHAR(100) NOT NULL,
  PRIMARY KEY (user_id),
  UNIQUE (email)
);

CREATE TABLE Tables_Dim
(
  table_id INT NOT NULL,
  seating_capacity INT NOT NULL,
  location VARCHAR(100),
  PRIMARY KEY (table_id)
);

CREATE TABLE Sales_Fact
(
  quantity INT NOT NULL,
  total_sale_amount FLOAT NOT NULL,
  order_id CHAR(5) NOT NULL,
  order_details_id CHAR(5) NOT NULL,
  menu_id INT NOT NULL,
  user_id INT NOT NULL,
  date_id_day INT NOT NULL,
  date_id_month INT NOT NULL,
  date_id_year INT NOT NULL,
  PRIMARY KEY (order_id, order_details_id),
  FOREIGN KEY (menu_id) REFERENCES Menu_Dim(menu_id),
  FOREIGN KEY (user_id) REFERENCES User_Dim(user_id),
  FOREIGN KEY (date_id_day, date_id_month, date_id_year) REFERENCES Date_Dim(day, month, year),
  UNIQUE (order_details_id)
);

CREATE TABLE Reservation_Fact
(
  reservation_id INT NOT NULL,
  no_of_guest INT NOT NULL,
  time INT NOT NULL,
  date_id_day INT NOT NULL,
  date_id_month INT NOT NULL,
  date_id_year INT NOT NULL,
  table_id INT NOT NULL,
  user_id INT NOT NULL,
  PRIMARY KEY (reservation_id),
  FOREIGN KEY (date_id_day, date_id_month, date_id_year) REFERENCES Date_Dim(day, month, year),
  FOREIGN KEY (table_id) REFERENCES Tables_Dim(table_id),
  FOREIGN KEY (user_id) REFERENCES User_Dim(user_id)
);
