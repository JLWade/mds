ALTER TABLE mine_detail DROP CONSTRAINT mine_detail_mine_region_fkey;

COMMIT;

DROP TABLE mine_detail;