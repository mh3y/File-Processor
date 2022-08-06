operation
SELECT
    Person.Person.FirstName,
    Person.Person.LastName,
    e.Gender,
    e.HireDate,
    e.BirthDate
FROM
HumanResources.Employee
INNER JOIN
Person.Person
ON
e.BusinessEntityID = Person.Person.BusinessEntityID
