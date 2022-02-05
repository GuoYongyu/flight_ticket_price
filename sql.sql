CREATE DATABASE airline_tickets;

CREATE TABLE `flight_price_records`.`Untitled`  (
  `index` int NOT NULL,
  `update_datetime` datetime NOT NULL,
  `departure_place` text NOT NULL,
  `destination_place` text NOT NULL,
  `airline_company` text NOT NULL,
  `airline_name` text NOT NULL,
  `plane_type` text NOT NULL,
  `departure_airport` text NOT NULL,
  `departure_time` datetime NOT NULL,
  `destination_airport` text NOT NULL,
  `arrival_time` datetime NOT NULL,
  `transfer_station` text NOT NULL,
  `cross_days` text NOT NULL,
  `travel_time` text NOT NULL,
  `ticket_price` text NOT NULL
);