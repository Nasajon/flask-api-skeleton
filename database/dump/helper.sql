--Exportar dados das tabelas para bulk no elastic

--PUT faturamento.pessoa/_bulk
select '{ "index": { "_id": "'||id||'" }}{ "resumo" : "'||codigo||' '||nome||' '||documento||'" }'  from faturamento.pessoa