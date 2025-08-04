-- Transform users data into normalized form
TRUNCATE TABLE ods_users;

INSERT INTO ods_users (
    firstname,
    lastname,
    latitude,
    longitude,
    street_number,
    street_name,
    zipcode
)
SELECT 
    name->>'firstname' as firstname,
    name->>'lastname' as lastname,
    (address->>'lat')::DECIMAL as latitude,
    (address->>'long')::DECIMAL as longitude,
    address->>'number' as street_number,
    address->>'street' as street_name,
    address->>'zipcode' as zipcode
FROM users;