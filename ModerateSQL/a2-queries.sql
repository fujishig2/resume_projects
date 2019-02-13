.print Question 1 -fujishig
SELECT c.local_contact
FROM service_agreements c, accounts d, personnel e
WHERE c.waste_type = "hazardous waste"
AND e.name = "Dan Brown"
AND d.account_mgr = e.pid
AND c.master_account = d.account_no;


.print \nQuestion 2 -fujishig
SELECT c.customer_name, c.contact_info, d.name AS 'Account manager'
FROM accounts c, personnel d
WHERE c.account_mgr = d.pid
AND c.end_date < (SELECT date('now', '+30 days'));

.print \nQuestion 3 -fujishig
SELECT c.customer_name
FROM accounts c, service_agreements d
WHERE c.account_no = d.master_account
AND  d.waste_type = "mixed waste"

EXCEPT

SELECT c.customer_name
FROM accounts c, service_agreements d
WHERE c.account_no = d.master_account
AND d.waste_type = "paper";

.print \nQuestion 4 -fujishig
SELECT c.manager_title AS 'Account Type', COUNT(d.service_no) AS 'Number of Services', SUM(d.price) - SUM(d.internal_cost) AS 'Profit'
FROM account_managers c, service_agreements d, accounts e
WHERE c.pid = e.account_mgr
AND e.account_no = d.master_account
GROUP BY c.manager_title;

.print \nQuestion 5 -fujishig
SELECT c.name
FROM personnel c, drivers d, service_fulfillments e
WHERE c.pid = d.pid
AND e.driver_id = d.pid
GROUP BY c.name
HAVING COUNT(e.driver_id) > 10;

.print \nQuestion 6 -fujishig
SELECT c.container_id
FROM containers c, service_fulfillments d
WHERE c.container_id = d.cid_drop_off
AND c.date_when_built < (SELECT date('now', '-5 years'))
GROUP BY c.container_id
HAVING COUNT(d.cid_drop_off) > 10;

.print \nQuestion 7 -fujishig.

SELECT c.container_id
FROM containers c

EXCEPT

SELECT c.container_id
FROM containers c, service_fulfillments d
WHERE c.container_id = d.cid_drop_off

UNION

SELECT c.container_id
FROM containers c, service_fulfillments d, service_fulfillments e
WHERE c.container_id = d.cid_pick_up
AND c.container_id = e.cid_drop_off
GROUP BY c.container_id
HAVING d.date_time > e.date_time;

.print \nQuestion 8 -fujishig
SELECT c.driver_id
FROM service_fulfillments c, accounts d
WHERE c.master_account = d.account_no
GROUP BY c.driver_id
HAVING NOT c.driver_id = 23769
AND (SELECT e.master_account
    FROM service_fulfillments e, accounts f
    WHERE e.master_account = d.account_no
    AND e.driver_id = 23769) = c.master_account;

.print \nQuestion 9 -fujishig
CREATE VIEW last2_inspections_of_company_trucks
       AS SELECT DISTINCT c.truck_id, c.truck_type, d.service_date AS inspection_date
       FROM trucks c, maintenance_records d, drivers e
       WHERE NOT e.owned_truck_id = c.truck_id
       AND c.truck_id = d.truck_id

       EXCEPT

       SELECT DISTINCT c.truck_id, c.truck_type, d.service_date AS inspection_date
       FROM trucks c, maintenance_records d, drivers e, maintenance_records f, maintenance_records g
       WHERE NOT e.owned_truck_id = c.truck_id
       AND c.truck_id = d.truck_id
       AND f.truck_id = c.truck_id
       AND g.truck_id = c.truck_id
       AND d.service_date < f.service_date
       AND f.service_date < g.service_date;

.print \nQuestion 10 -fujishig
SELECT c.truck_type, MIN(julianday(c.inspection_date) - julianday(d.inspection_date)) AS Minimum, MAX(julianday(c.inspection_date) - julianday(d.inspection_date)) AS Maximum, AVG(julianday(c.inspection_date) - julianday(d.inspection_date)) AS Average
FROM last2_inspections_of_company_trucks c, last2_inspections_of_company_trucks d
WHERE c.truck_id = d.truck_id
AND c.inspection_date > d.inspection_date
GROUP BY c.truck_type;
