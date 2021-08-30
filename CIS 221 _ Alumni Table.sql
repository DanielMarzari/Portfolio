CREATE TABLE Alumni (
	ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
	FirstName VARCHAR(100) NOT NULL,
	LastName VARCHAR(100) NOT NULL,
	CairnDegree VARCHAR(255) NOT NULL,
	GraduationYear INT NOT NULL, 
	LinkedInURL VARCHAR(255) NOT NULL,
	CurrentEmployment VARCHAR(255) NOT NULL,
	Address VARCHAR(255),
	Phone VARCHAR(30), -- this should avoid all odd formatting errors and extensions
	Email VARCHAR(100),
	OtherDegrees VARCHAR(255),
	Internship VARCHAR(255),
	SpeakingHistory VARCHAR(255),
	Notes VARCHAR(255) -- shouldn't exceed 255 characters
) ENGINE InnoDB DEFAULT CHARSET=latin1;
