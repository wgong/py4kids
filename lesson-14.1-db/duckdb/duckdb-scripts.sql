select * from daily_quote;
describe daily_quote;

select count(*) from daily_quote;
--35960

select "<PER>",count(*) from daily_quote group by "<PER>";
/*
5	21970
D	12055
60	1935
 */

select count(*) from daily_quote where "<PER>" = 'D';
--12055

create table daily_quote_d as select * from daily_quote  where "<PER>" = 'D';

show tables;

select * from daily_quote_d;

select count(*) from daily_quote_d where "<TICKER>" like '^%';
--57

select count(*) from daily_quote_d where "<TICKER>" like '%.US';
--7999

select * from daily_quote_d where "<TICKER>" like '%.US' order by "<TICKER>";

select count(*) from daily_quote_d where "<TICKER>" like '%.JP';
--3872


select * from daily_quote_2;

select count(*) from daily_quote_2;

drop table daily_quote_2;