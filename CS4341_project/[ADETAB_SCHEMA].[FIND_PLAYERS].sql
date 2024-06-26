USE [ADETAB_DB]
GO
/****** Object:  StoredProcedure [ADETAB_SCHEMA].[FIND_PLAYERS]    Script Date: 12/17/2023 9:25:37 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
/*
select * from [dbo].[NBA_Team_Stats_malik]
select * from ADETAB_Db.ADETAB_SCHEMA.malik

drop table #temp_teams
select row_number() over (partition by [Year] order by Team asc) as TEAM_ID, Team, 500000 + floor(60000000 * RAND(convert(varbinary, newid()))) CapSpace
into #temp_teams
from [dbo].[NBA_Team_Stats_malik]
where [year] like '2021-2022'
insert #temp_teams values (30, 'Houston', floor(60000000 * RAND(convert(varbinary, newid()))))
select * from #temp_teams


select * from #temp_players
select AVG(PTS) AVGPTS, AVG(REB) AVGREB, AVG(AST) AVGAST, AVG(STL) AVGSTL, AVG(BLK) AVGBLK from #temp_PLAYERS

/*
7.816438	3.324533	1.811332	0.583686	0.353673
select @need_PTS
select @need_REB
select @need_AST
select @need_STL
select @need_BLK

*/


*/

--use ADETAB_DB


ALTER PROCEDURE [ADETAB_SCHEMA].[FIND_PLAYERS] 

--DECLARE 
@ignore_salary_cap INTEGER = 1 --1 = Yes, 0 = No

AS

-- exec [ADETAB_SCHEMA].[FIND_PLAYERS] 1

drop table if exists #temp_players
select row_number() over (partition by Season order by Tm asc) as Player_ID, Player, Tm Team, Pos, 
Age, G, GS, MP, CONVERT(DECIMAL(5,1), PTS) PTS, CONVERT(DECIMAL(5,1), TRB) REB, CONVERT(DECIMAL(5,1), AST) AST, 
CONVERT(DECIMAL(5,1), STL) STL, CONVERT(DECIMAL(5,1), BLK) BLK, 500000 + floor(60000000 * RAND(convert(varbinary, newid()))) Salary
into #temp_players
from ADETAB_Db.ADETAB_SCHEMA.malik
where Season like '2021-22'

drop table if exists #starting_lineup
select top 4 *, 'Original Lineup' PlayerType 
into #starting_lineup
from #temp_players
where player in ('Tyrese Maxey','Patty Mills','Jalen Green','Marcus Garrett')
order by newid()

DECLARE @current_total_salary INTEGER;
SELECT @current_total_salary = SUM(Salary) FROM #starting_lineup

DECLARE @ovr_avg_pts DECIMAL(5,1);
DECLARE @ovr_avg_reb DECIMAL(5,1);
DECLARE @ovr_avg_ast DECIMAL(5,1);
DECLARE @ovr_avg_stl DECIMAL(5,1);
DECLARE @ovr_avg_blk DECIMAL(5,1);

DECLARE @avg_pts DECIMAL(5,1);
DECLARE @avg_reb DECIMAL(5,1);
DECLARE @avg_ast DECIMAL(5,1);
DECLARE @avg_stl DECIMAL(5,1);
DECLARE @avg_blk DECIMAL(5,1);

SELECT 
	@ovr_avg_pts = AVG(PTS),
	@ovr_avg_reb = AVG(REB),
	@ovr_avg_ast = AVG(AST),
	@ovr_avg_stl = AVG(STL),
	@ovr_avg_blk = AVG(BLK)
FROM 
	#temp_players

SELECT 
	@avg_pts = AVG(PTS),
	@avg_reb = AVG(REB),
	@avg_ast = AVG(AST),
	@avg_stl = AVG(STL),
	@avg_blk = AVG(BLK)
FROM 
	#starting_lineup



DECLARE @need_pts INTEGER = 0;
DECLARE @need_reb INTEGER = 0;
DECLARE @need_ast INTEGER = 0;
DECLARE @need_stl INTEGER = 0;
DECLARE @need_blk INTEGER = 0;

IF @avg_pts < @ovr_avg_pts
BEGIN
	SELECT @need_pts = 1;
END

IF @avg_reb < @ovr_avg_reb
BEGIN
	SELECT @need_reb = 1;
END

IF @avg_ast < @ovr_avg_ast
BEGIN
	SELECT @need_ast = 1;
END

IF @avg_stl < @ovr_avg_stl
BEGIN
	SELECT @need_stl = 1;
END

IF @avg_blk < @ovr_avg_blk
BEGIN
	SELECT @need_blk = 1;
END



--RESULTS--
-----------
/*SELECT
	* 
FROM
	#starting_lineup s*/


DROP TABLE IF EXISTS adetab_db.adetab_schema.jsons
SELECT TOP 1
	*, 'Recommended Player' PlayerType
INTO
	adetab_db.adetab_schema.jsons
FROM
	#temp_players p
WHERE 
	 ( (@need_pts = 1 
	 AND (@avg_pts * 4 + p.PTS) / 5 > @ovr_avg_pts) OR @need_pts = 0 )

	 AND ( (@need_ast = 1 
	 AND (@avg_ast * 4 + p.AST) / 5 > @ovr_avg_ast) OR @need_ast = 0 )

	 AND ( (@need_reb = 1 
	 AND (@avg_reb * 4 + p.REB) / 5 > @ovr_avg_reb) OR @need_reb = 0 )

	 AND ( (@need_stl = 1 
	 AND (@avg_stl * 4 + p.STL) / 5 > @ovr_avg_stl) OR @need_stl = 0 )

	 AND ( (@need_blk = 1 
	 AND (@avg_blk * 4 + p.BLK) / 5 > @ovr_avg_blk) OR @need_blk = 0 )

	 AND ( (@ignore_salary_cap = 0
	 AND @current_total_salary + p.Salary < 136000000) OR @ignore_salary_cap = 1 ) --NBA Salary Cap is 136,000,000
ORDER BY 
	PTS ASC


DROP TABLE IF EXISTS adetab_db.adetab_schema.json_final
;WITH storejson(a) as (
SELECT
	Player, Team, Pos, Age, G, GS, MP, PTS, REB, AST, STL,
	BLK, CONVERT(INTEGER, Salary) AS Salary
FROM 
	adetab_db.adetab_schema.jsons FOR JSON AUTO
)
SELECT 
	a
INTO
	adetab_db.adetab_schema.json_final
FROM
	storejson

--select * from adetab_db.adetab_schema.jsons_final
--exec [ADETAB_SCHEMA].[FIND_PLAYERS] 1