-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Apr 15, 2025 at 07:24 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `omgl_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `challenges`
--

CREATE TABLE `challenges` (
  `id` int(11) NOT NULL,
  `type` varchar(255) NOT NULL,
  `question` varchar(255) NOT NULL,
  `options` varchar(255) NOT NULL,
  `correct_answer` varchar(255) NOT NULL,
  `reward_keys` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `challenges`
--

INSERT INTO `challenges` (`id`, `type`, `question`, `options`, `correct_answer`, `reward_keys`) VALUES
(1, 'quiz', 'what is 3+(9/3) = ?', '6;3;4;0', '6', 5),
(2, 'code', 'In C++ user input and output which library we used?', 'iostream;conio;printf;cout', 'iostream', 10),
(3, 'scenario', 'If the A is greater then B and B is less than C.Then what equation is correct', 'A>B<C', 'A>B<C', 15),
(4, 'quiz', 'what is factorial of 5!', '40;20;5;9', '40', 2);

-- --------------------------------------------------------

--
-- Table structure for table `user_progress`
--

CREATE TABLE `user_progress` (
  `UserID` varchar(255) NOT NULL,
  `userkeys` varchar(255) NOT NULL,
  `global_time` varchar(255) NOT NULL,
  `completed_challenges` varchar(255) NOT NULL,
  `id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `user_progress`
--

INSERT INTO `user_progress` (`UserID`, `userkeys`, `global_time`, `completed_challenges`, `id`) VALUES
('M304964150', '20', '02:44', 'Won', 1),
('M784940378', '0', '02:59', 'Won', 2),
('M473171502', '5', '04:19', 'Won', 3),
('M191515573', '2', '04:41', 'Won', 4),
('M113407476', '3', '01:36', 'Won', 5),
('M856694509', '7', '01:25', 'Won', 6),
('M16399429', '2', '03:37', 'Won', 7),
('M68443713', '15', '05:02', 'Won', 8),
('M528035045', '22', '09:40', 'Won', 9),
('M542795410', '14', '10:12', 'Won', 10);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `challenges`
--
ALTER TABLE `challenges`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `user_progress`
--
ALTER TABLE `user_progress`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `challenges`
--
ALTER TABLE `challenges`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `user_progress`
--
ALTER TABLE `user_progress`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
