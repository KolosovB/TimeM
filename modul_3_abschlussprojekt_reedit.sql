--
-- Datenbank: `modul_3_abschlussprojekt`
--
-- Erstellen Database "modul_3_abschlussprojekt" für Firma "Finck & Maier IT Consulting GmbH"
-- Als Charset benutzen wir "utf8_general_ci" um Unicode Zeichen richtig zu anzeigen
--
DROP DATABASE IF EXISTS modul_3_abschlussprojekt;
CREATE DATABASE modul_3_abschlussprojekt;
USE modul_3_abschlussprojekt;

--
-- Tabellenstruktur für Tabelle `Abteilung`
--
DROP TABLE IF EXISTS Abteilung;
CREATE TABLE Abteilung (
  Abteilung_ID tinyint NOT NULL PRIMARY KEY IDENTITY(1,1),
  Abteilung_name varchar(30) NOT NULL);

--
-- Daten für Tabelle `Abteilung`
--

INSERT INTO Abteilung (Abteilung_name) VALUES
(Geschäftsführung),
(Verwaltung),
(Technik);

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `Adresse`
--
DROP TABLE IF EXISTS Adresse;
CREATE TABLE Adresse (
  Adresse_ID tinyint NOT NULL PRIMARY KEY IDENTITY(1,1),
  Straße varchar(50) NOT NULL,
  HausNr tinyint NOT NULL,
  Ort varchar(50) NOT NULL,
  PLZ char(5) DEFAULT NULL
);

--
-- Daten für Tabelle `adresse`
--

INSERT INTO Adresse (Adresse_ID, Straße, HausNr, Ort, PLZ) VALUES
(1, 'Musterstraße', 12, 'Berlin', '10115'),
(2, 'Beispielweg', 45, 'Berlin', '10437'),
(3, 'Testplatz', 8, 'Berlin', '10789'),
(4, 'Probeweg', 23, 'Berlin', '10247'),
(5, 'Musterweg', 56, 'Berlin', '10967'),
(6, 'Beispielallee', 33, 'Berlin', '10119'),
(7, 'Teststraße', 72, 'Berlin', '10405'),
(8, 'Probeweg', 14, 'Berlin', '10777'),
(9, 'Musterplatz', 89, 'Berlin', '10827'),
(10, 'Beispielweg', 17, 'Berlin', '10178'),
(11, 'Testplatz', 41, 'Berlin', '10969'),
(12, 'Probeweg', 99, 'Berlin', '10318'),
(13, 'Musterweg', 62, 'Berlin', '10245'),
(14, 'Beispielplatz', 7, 'Berlin', '10623'),
(15, 'Testallee', 21, 'Berlin', '10587'),
(16, 'Probeweg', 37, 'Berlin', '10435'),
(17, 'Musterplatz', 44, 'Berlin', '10823'),
(18, 'Beispielstraße', 29, 'Berlin', '10117'),
(19, 'Testweg', 83, 'Berlin', '10785'),
(20, 'Probeweg', 51, 'Berlin', '10369');

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `Arbeitsvertrag`
--
DROP TABLE IF EXISTS Arbeitsvertrag;
CREATE TABLE Arbeitsvertrag(
  Arbeitsvertrag_ID tinyint NOT NULL PRIMARY KEY IDENTITY(1,1),
  Vertragsbeginn date DEFAULT NULL,
  Vertragsende date DEFAULT NULL,
  Beschäftigung_ID tinyint NOT NULL,
  Vertragsart_ID tinyint DEFAULT NULL
);

--
-- Daten für Tabelle `Arbeitsvertrag`
--
INSERT INTO Arbeitsvertrag (Vertragsbeginn, Vertragsende, Beschäftigung_ID, Vertragsart_ID) VALUES
('2010-06-11', NULL, 1, 2),
('2010-06-11', NULL, 1, 2),
('2014-06-12', NULL, 1, 2),
('2018-06-14', NULL, 2, 2),
('2012-06-08', NULL, 1, 2),
('2016-06-10', NULL, 1, 2),
('2021-06-11', NULL, 1, 2),
('2022-11-21', '2024-06-17', 2, 1),
('2013-06-15', NULL, 1, 2),
('2017-06-17', NULL, 1, 2),
('2014-10-10', NULL, 1, 2),
('2022-11-21', '2024-06-17', 1, 1),
('2013-03-19', NULL, 1, 2),
('2017-12-14', NULL, 1, 2),
('2014-06-03', NULL, 2, 2),
('2020-08-18', NULL, 1, 2),
('2020-08-18', NULL, 1, 2),
('2022-11-21', NULL, 1, 2),
('2021-06-11', NULL, 2, 2),
('2022-11-21', '2024-06-17', 1, 1);

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `Arbeitszeiten`
--
DROP TABLE IF EXISTS Arbeitszeiten;
CREATE TABLE Arbeitszeiten (
  Antrag_ID tinyint NOT NULL PRIMARY KEY IDENTITY(1,1),
  Mitarbeiter_ID tinyint NOT NULL,
  Tag date DEFAULT NULL,
  Startzeit time DEFAULT NULL,
  Endzeit time DEFAULT NULL,
  Tarif_ID tinyint NOT NULL,
  Überstunden int(11) DEFAULT NULL
);

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `Beschäftigung`
--
DROP TABLE IF EXISTS Beschäftigung;
CREATE TABLE Beschäftigung (
  Beschäftigung_ID tinyint NOT NULL PRIMARY KEY IDENTITY(1,1),
  Beschäftigung_name varchar(10) NOT NULL
);

--
-- Daten für Tabelle `beschäftigung`
--
INSERT INTO `Beschäftigung` (`Beschäftigung_name`) VALUES
('Vollzeit'),
('Teilzeit'),
('Basis'),
('Projekt');

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `Kontotype`
--
DROP TABLE IF EXISTS `Kontotype`;
CREATE TABLE `Kontotype` (
  `Kontotype_ID` tinyint(4) NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `Kontotype_name` varchar(20) NOT NULL
) DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Daten für Tabelle `Kontotype`
--

INSERT INTO `Kontotype` (`Kontotype_name`) VALUES
('Administrator'),
('Buchhaltung'),
('Benutzer'),
('Geblockt');

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `Login`
--
DROP TABLE IF EXISTS `Login`;
CREATE TABLE `Login` (
  `Login_ID` tinyint(4) NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `E_Mail` varchar(50) NOT NULL,
  `Password` varchar(50) DEFAULT NULL
) DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Daten für Tabelle `Login`
--
INSERT INTO `Login` (`E_Mail`, `Password`) VALUES
('joerg.finck@finck-maier-consulting.de', '8e8c11dc6e823ef7a1a98f0009d1a6c6'),
('olga.maier@finck-maier-consulting.de', '8e8c11dc6e823ef7a1a98f0009d1a6c6'),
('michael.schneider@finck-maier-consulting.de', '907fd7e6b571e52bc8670b305acc34af'),
('lisa.zimmermann@finck-maier-consulting.de', '907fd7e6b571e52bc8670b305acc34af'),
('julia.becker@finck-maier-consulting.de', '907fd7e6b571e52bc8670b305acc34af'),
('markus.weber@finck-maier-consulting.de', '907fd7e6b571e52bc8670b305acc34af'),
('laura.schmitz@finck-maier-consulting.de', '34a345f5a745f27e3256cccc77a3bc68'),
('timo.fischer@finck-maier-consulting.de', '907fd7e6b571e52bc8670b305acc34af'),
('andreas.richter@finck-maier-consulting.de', '907fd7e6b571e52bc8670b305acc34af'),
('sabine.mueller@finck-maier-consulting.de', '907fd7e6b571e52bc8670b305acc34af'),
('alexander.weber@finck-maier-consulting.de', '907fd7e6b571e52bc8670b305acc34af'),
('melanie.schulz@finck-maier-consulting.de', '907fd7e6b571e52bc8670b305acc34af'),
('christian.mueller@finck-maier-consulting.de', '907fd7e6b571e52bc8670b305acc34af'),
('niklas.becker@finck-maier-consulting.de', '907fd7e6b571e52bc8670b305acc34af'),
('lisa.schaefer@finck-maier-consulting.de', '907fd7e6b571e52bc8670b305acc34af'),
('sebastian.vogel@finck-maier-consulting.de', '907fd7e6b571e52bc8670b305acc34af'),
('patrick.keller@finck-maier-consulting.de', '907fd7e6b571e52bc8670b305acc34af'),
('daniel.hoffmann@finck-maier-consulting.de', '907fd7e6b571e52bc8670b305acc34af'),
('laura.mayer@finck-maier-consulting.de', '907fd7e6b571e52bc8670b305acc34af'),
('tobias.schmit@finck-maier-consulting.de', '907fd7e6b571e52bc8670b305acc34af');

-- --------------------------------------------------------
--
-- Tabellenstruktur für Tabelle `Mitarbeiter`
--
DROP TABLE IF EXISTS `Mitarbeiter`;
CREATE TABLE `Mitarbeiter`(
  `Mitarbeiter_ID` tinyint(4) NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `Vorname` varchar(50) NOT NULL,
  `Nachname` varchar(50) NOT NULL,
  `Geburtsdatum` date DEFAULT NULL,
  `Telefonnummer` int(8) DEFAULT NULL,
  `Adresse_ID` tinyint(4) NOT NULL,
  `Login_ID` tinyint(4) NOT NULL,
  `Kontotype_ID` tinyint(4) DEFAULT NULL,
  `Abteilung_ID` tinyint(4) NOT NULL,
  `Position_ID` tinyint(4) NOT NULL,
  `Arbeitsvertrag_ID` tinyint(4) NOT NULL
) DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Daten für Tabelle `mitarbeiter`
--

INSERT INTO `Mitarbeiter` (`Vorname`, `Nachname`, `Geburtsdatum`, `Telefonnummer`, `Adresse_ID`, `Login_ID`, `Kontotype_ID`, `Abteilung_ID`, `Position_ID`, `Arbeitsvertrag_ID`) VALUES
('Jörg', 'Fink', '1980-12-03', '30456760', 1, 1, 1, 1, 1, 1),
('Olga', 'Maier', '1988-05-03', '30456761', 2, 2, 1, 1, 1, 2),
('Michael', 'Schneider', '1970-06-21', '30456770', 3, 3, 3, 2, 2, 3),
('Lisa', 'Zimmermann', '1974-07-07', '30456771', 4, 4, 3, 2, 3, 4),
('Julia', 'Becker', '1978-06-25', '30456772', 5, 5, 3, 2, 4, 5),
('Markus', 'Weber', '1982-07-11', '30456773', 6, 6, 3, 2, 5, 6),
('Laura', 'Schmitz', '1986-06-29', '30456774', 7, 7, 2, 2, 6, 7),
('Timo', 'Fischer', '1990-07-08', '30456775', 8, 8, 3, 2, 7, 8),
('Andreas', 'Richter', '1994-07-17', '30456780', 9, 9, 3, 3, 8, 9),
('Sabine', 'Müller', '1998-07-12', '30456781', 10, 10, 3, 3, 9, 10),
('Alexander', 'Weber', '1972-06-18', '30456782', 11, 11, 3, 3, 10, 11),
('Melanie', 'Schulz', '1976-06-20', '30456783', 12, 12, 3, 3, 11, 12),
('Christian', 'Müller', '1980-06-22', '30456784', 13, 13, 3, 3, 12, 13),
('Niklas', 'Becker', '1984-06-27', '30456785', 14, 14, 3, 3, 12, 14),
('Lisa', 'Schäfer', '1988-06-25', '30456786', 15, 15, 3, 3, 13, 15),
('Sebastian', 'Vogel', '1992-06-26', '30456787', 16, 16, 3, 3, 13, 16),
('Patrick', 'Keller', '1996-06-30', '30456790', 17, 17, 3, 3, 14, 17),
('Daniel', 'Hoffmann', '2000-07-02', '30456791', 18, 18, 3, 3, 15, 18),
('Laura', 'Mayer', '2002-06-30', '30456792', 19, 19, 3, 3, 15, 19),
('Tobias', 'Schmit', '2004-06-04', '30456793', 20, 20, 4, 3, 15, 20);

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `position`
--
DROP TABLE IF EXISTS `Position`;
CREATE TABLE `Position` (
  `Position_ID` tinyint(4) NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `Position_name` varchar(50) NOT NULL
) DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Daten für Tabelle `position`
--

INSERT INTO `Position` (`Position_name`) VALUES
('Geschäftsführung'),
('HR-Leiter'),
('Personalreferentin'),
('Gehaltsbuchhalterin'),
('Finanzleiter'),
('Controller'),
('Buchhalter'),
('IT-Projektmanager'),
('Senior IT-Berater'),
('Systemadministrator Leiter'),
('Datenbankexperte'),
('Netzwerkarchitekt'),
('Systemadministrator'),
('IT-Support Leiter'),
('IT-Support');

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `Tarif`
--
DROP TABLE IF EXISTS `Tarif`;
CREATE TABLE `Tarif` (
  `Tarif_ID` tinyint(4) NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `Tarif_name` varchar(20) NOT NULL
) DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Daten für Tabelle `tarif`
--

INSERT INTO `Tarif` (`Tarif_name`) VALUES
('Normal'),
('Überstunden'),
('Krank'),
('Kind Krank'),
('Urlaub');

--
-- Tabellenstruktur für Tabelle `Vertragsart`
--
DROP TABLE IF EXISTS `Vertragsart`;
CREATE TABLE `Vertragsart` (
  `Vertragsart_ID` tinyint(4) NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `Vertragsart_name` varchar(50) DEFAULT NULL
) DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Daten für Tabelle `vertragsart`
--

INSERT INTO `Vertragsart` (`Vertragsart_name`) VALUES
('Befristet'),
('Unbefristet');

--
-- Indizes für die Tabelle `arbeitsvertrag`
--
ALTER TABLE `Arbeitsvertrag`
  ADD KEY `beschäftigung_id_fk` (`Beschäftigung_ID`),
  ADD KEY `vertragsart_id_fk` (`Vertragsart_ID`);

--
-- Indizes für die Tabelle `arbeitszeiten`
--
ALTER TABLE `Arbeitszeiten`
  ADD KEY `mitarbeiter_id_fk` (`Mitarbeiter_ID`),
  ADD KEY `tarif_id_fk` (`Tarif_ID`);


--
-- Indizes für die Tabelle `mitarbeiter`
--
ALTER TABLE `mitarbeiter`
  ADD KEY `adresse_id_fk` (`Adresse_ID`),
  ADD KEY `login_id_fk` (`Login_ID`),
  ADD KEY `kontotype_id_fk` (`Kontotype_ID`),
  ADD KEY `abteilung_id_fk` (`Abteilung_ID`),
  ADD KEY `position_id_fk` (`Position_ID`),
  ADD KEY `arbeitsvertrag_id_fk` (`Arbeitsvertrag_ID`);

--
-- Constraints der Tabelle `arbeitsvertrag`
--
ALTER TABLE `Arbeitsvertrag`
  ADD CONSTRAINT `beschäftigung_id_fk` FOREIGN KEY (`Beschäftigung_ID`) REFERENCES `Beschäftigung` (`Beschäftigung_ID`),
  ADD CONSTRAINT `vertragsart_id_fk` FOREIGN KEY (`Vertragsart_ID`) REFERENCES `Vertragsart` (`Vertragsart_ID`);

--
-- Constraints der Tabelle `arbeitszeiten`
--
ALTER TABLE `Arbeitszeiten`
  ADD CONSTRAINT `mitarbeiter_id_fk` FOREIGN KEY (`Mitarbeiter_ID`) REFERENCES `Mitarbeiter` (`Mitarbeiter_ID`),
  ADD CONSTRAINT `tarif_id_fk` FOREIGN KEY (`Tarif_ID`) REFERENCES `Tarif` (`Tarif_ID`);

--
-- Constraints der Tabelle `mitarbeiter`
--
ALTER TABLE `Mitarbeiter`
  ADD CONSTRAINT `abteilung_id_fk` FOREIGN KEY (`Abteilung_ID`) REFERENCES `Abteilung` (`Abteilung_ID`),
  ADD CONSTRAINT `adresse_id_fk` FOREIGN KEY (`Adresse_ID`) REFERENCES `Adresse` (`Adresse_ID`),
  ADD CONSTRAINT `arbeitsvertrag_id_fk` FOREIGN KEY (`Arbeitsvertrag_ID`) REFERENCES `Arbeitsvertrag` (`Arbeitsvertrag_ID`),
  ADD CONSTRAINT `kontotype_id_fk` FOREIGN KEY (`Kontotype_ID`) REFERENCES `Kontotype` (`Kontotype_ID`),
  ADD CONSTRAINT `login_id_fk` FOREIGN KEY (`Login_ID`) REFERENCES `Login` (`Login_ID`),
  ADD CONSTRAINT `position_id_fk` FOREIGN KEY (`Position_ID`) REFERENCES `Position` (`Position_ID`);
COMMIT;

ALTER TABLE arbeitsvertrag
ADD Gehalt VARCHAR(50);
 
UPDATE arbeitsvertrag 
SET Gehalt = '165.000,00 €' 
WHERE Arbeitsvertrag_ID = 1;
 
UPDATE arbeitsvertrag 
SET Gehalt = '165.000,00 €' 
WHERE Arbeitsvertrag_ID = 2;
 
UPDATE arbeitsvertrag 
SET Gehalt = '43.562,00 €' 
WHERE Arbeitsvertrag_ID = 3;
 
UPDATE arbeitsvertrag 
SET Gehalt = '27.290,00 €' 
WHERE Arbeitsvertrag_ID = 4;
 
UPDATE arbeitsvertrag 
SET Gehalt = '44.450,00 €' 
WHERE Arbeitsvertrag_ID = 5;
 
UPDATE arbeitsvertrag 
SET Gehalt = '40.680,00 €' 
WHERE Arbeitsvertrag_ID = 6;
 
UPDATE arbeitsvertrag 
SET Gehalt = '30.680,00 €' 
WHERE Arbeitsvertrag_ID = 7;
 
UPDATE arbeitsvertrag 
SET Gehalt = '40.150,00 €' 
WHERE Arbeitsvertrag_ID = 8;
 
UPDATE arbeitsvertrag 
SET Gehalt = '60.300,00 €' 
WHERE Arbeitsvertrag_ID = 9;
 
UPDATE arbeitsvertrag 
SET Gehalt = '36.782,00 €' 
WHERE Arbeitsvertrag_ID = 10;
 
UPDATE arbeitsvertrag 
SET Gehalt = '57.200,00 €' 
WHERE Arbeitsvertrag_ID = 11;
 
UPDATE arbeitsvertrag 
SET Gehalt = '30.397,00 €' 
WHERE Arbeitsvertrag_ID = 12;
 
UPDATE arbeitsvertrag 
SET Gehalt = '39.042,00 €' 
WHERE Arbeitsvertrag_ID = 13;
 
UPDATE arbeitsvertrag 
SET Gehalt = '39.042,00 €' 
WHERE Arbeitsvertrag_ID = 14;
 
UPDATE arbeitsvertrag 
SET Gehalt = '44.700,00 €' 
WHERE Arbeitsvertrag_ID = 15;
 
UPDATE arbeitsvertrag 
SET Gehalt = '44.700,00 €' 
WHERE Arbeitsvertrag_ID = 16;
 
UPDATE arbeitsvertrag 
SET Gehalt = '40.285,00 €' 
WHERE Arbeitsvertrag_ID = 17;
 
UPDATE arbeitsvertrag 
SET Gehalt = '39.000,00 €' 
WHERE Arbeitsvertrag_ID = 18;
 
UPDATE arbeitsvertrag 
SET Gehalt = '39.000,00 €' 
WHERE Arbeitsvertrag_ID = 19;
 
UPDATE arbeitsvertrag 
SET Gehalt = '39.000,00 €' 
WHERE Arbeitsvertrag_ID = 20;

INSERT INTO `arbeitszeiten`(`Mitarbeiter_ID`, `Tag`, `Startzeit`, `Endzeit`, `Tarif_ID`, `Überstunden`) VALUES 
('1','2024-02-01','8:00','19:00','1','60'),
('1','2024-02-02','8:00','19:00','1','60'),
('1','2024-02-05','8:00','19:00','1','60'),
('1','2024-02-06','8:00','19:00','1','60'),
('1','2024-02-07','8:00','19:00','1','60'),
('1','2024-02-08','8:00','19:00','1','60'),
('1','2024-02-09','8:00','19:00','1','60'),
('1','2024-02-12','8:00','19:00','1','60'),
('1','2024-02-13','8:00','19:00','1','60'),
('1','2024-02-14','8:00','19:00','1','60'),
('1','2024-02-15','8:00','19:00','1','60'),
('1','2024-02-16','8:00','19:00','1','60'),
('1','2024-02-19','8:00','19:00','1','60'),
('1','2024-02-20','8:00','19:00','1','60'),
('1','2024-02-21','8:00','19:00','1','60'),
('1','2024-02-22','8:00','19:00','1','60');

INSERT INTO `arbeitszeiten`(`Mitarbeiter_ID`, `Tag`, `Startzeit`, `Endzeit`, `Tarif_ID`, `Überstunden`) VALUES 
('5','2024-02-01','8:00','18:00','3','0'),
('5','2024-02-02','8:00','18:00','3','0'),
('5','2024-02-05','8:00','18:00','3','0'),
('5','2024-02-06','8:00','18:00','3','0'),
('5','2024-02-07','8:00','18:00','3','0'),
('5','2024-02-08','8:00','19:00','1','60'),
('5','2024-02-09','8:00','19:00','1','60'),
('5','2024-02-12','8:00','19:00','1','60'),
('5','2024-02-13','8:00','19:00','1','60'),
('5','2024-02-14','8:00','18:00','1','0'),
('5','2024-02-15','8:00','18:00','1','0'),
('5','2024-02-16','8:00','15:00','1','0'),
('5','2024-02-19','8:00','15:00','1','0'),
('5','2024-02-20','8:00','12:00','1','0'),
('5','2024-02-21','8:00','19:00','1','60'),
('5','2024-02-22','8:00','19:00','1','60');