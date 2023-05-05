Use MouseHypothalamus;

-- A small test table with cell names and ids for only one animal, one bregma, one z layer
-- SELECT DISTINCT cell_name, IDENTITY(int,1,1) as cell_id
--     INTO CellNamesOneAnimalOneBregmaOneZ
--     FROM [MouseHypothalamus].[dbo].[MoleculesWithPoints]
--     where 1 = Animal_ID and bregma = 0.21 and Centroid_Z = 3

-- Create the big table associating cell names with cell ids (in no particular order)
-- SELECT DISTINCT cell_name, IDENTITY(int,1,1) as cell_id
--     INTO CellNames
--     FROM [MouseHypothalamus].[dbo].[MoleculesWithPoints]

-- Join the cell ids with MoleculesWithPoints for hopefully faster queries later
-- SELECT m.id, m.gene_name, m.cell_name, n.cell_id, m.animal_id, m.bregma, m.centroid_Z, m.point as xy_point
--     INTO MoleculesWithPointsWithCellIds
--     FROM MoleculesWithPoints as m 
--     INNER JOIN CellNames as n 
--     ON m.Cell_name = n.cell_name

-- Join the existing cell ids from CellBoundaries with MoleculesWithPoints
DROP TABLE IF EXISTS MoleculesWithPointsWithCellIds
SELECT IDENTITY(int,1,1) as id, m.id as molecule_id, m.gene_name, m.cell_name, n.feature_id, m.animal_id, m.bregma, m.centroid_Z, m.point as xy_point
    INTO MoleculesWithPointsWithCellIds
    FROM MoleculesWithPoints as m 
    INNER JOIN CellBoundariesWithPolygons as n 
    ON m.Cell_name = n.feature_uID

ALTER TABLE MoleculesWithPointsWithCellIds
    ADD CONSTRAINT MoleculesWithPointsWithCellIds_id_PK PRIMARY KEY (id);

CREATE SPATIAL INDEX MoleculesWithPointsWithCellIdsInd ON
   [MouseHypothalamus].[dbo].[MoleculesWithPointsWithCellIds](xy_point)
   WITH (GRIDS = (HIGH, HIGH, HIGH, HIGH), 
        BOUNDING_BOX = (XMIN = -6000,YMIN = -6000, XMAX = 6000, YMAX = 6000)); -- rounding up to +- 6000