-- Ranks country origins of bands.
SELECT origin, COUNT(*) as fans_nb
FROM metal_bands
GROUP BY origin
ORDER BY fans_nb DESC;
