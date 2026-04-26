--All Rules On Product Level and Types in use
--'CFG_LEVEL'| PRODUCT_CODE | VERSION | RULE_CPR_ID | RULE_TYPE | RULE_CODE | FOLDER | DESCRIPTION
SELECT 'Product' AS CFG_LEVEL , p.product_code , pv.version
      , pr.rule_cpr_id AS RULE_ID, pr.rule_type_link_id AS Rule_Type -- pr.product_link_id
      , rr.rule_code, rr.folder, rr.description          
            FROM CFG_NL_PRODUCT_RULES pr -- pr.product_link_id, pr.rule_type_link_id AS Rule_Type, pr.rule_cpr_id
      JOIN CFG_NL_PRODUCT p ON pr.product_link_id = p.product_link_id
      JOIN CFG_NL_PRODUCT_VERSIONS pv ON pv.product_link_id = p.product_link_id       
      JOIN cpr_rules rr ON rr.rule_cpr_id = pr.rule_cpr_id
 WHERE 1=1 AND pr.rule_type_link_id like '%AMNT%'     --'DOC%'      
-- WHERE 1=1 AND pr.rule_type_link_id like 'PC_%NON%'     --'DOC%' 

-- INSIS_GEN_CFG_V10
SELECT * FROM CPR_RULES ;
SELECT * FROM CPRS_RULE_DEFINITION WHERE rule_proc IS NOT NULL ; -- KW
SELECT * FROM CPRS_RULE_FLDVALUES ;
SELECT * FROM CPRS_RULE_LMATH ;
SELECT * FROM CPRS_RULE_OPERATIONS ;
SELECT * FROM CPRS_RULE_RATING_ADDITION ;

SELECT * FROM CPRS_RULE_SEQUENTIAL s WHERE s.main_rule_id = ;
--SEQ with Rules inside of it
SELECT s.main_rule_id , s.cpr_rule_id 
      , r.rule_code -- , r.description 
      , s.rule_order , s.sequence_type , s.return_name
      FROM CPRS_RULE_SEQUENTIAL s 
      , CPR_RULES r
      WHERE s.main_rule_id = 3180011094  
      AND s.cpr_rule_id = r.rule_cpr_id ;
SELECT * FROM CPRS_RULE_TABLE_DEF ;
SELECT * FROM CPRS_RULE_TABLE_WHERE_CLAUSE ; -- KW
SELECT * FROM CPRS_RULE_VALIDATION_RESULTS ;
--Find a Keyword and its definition=statement
SELECT * FROM SYSCFG_RULE_KEYWORDS WHERE 1=1 
      --    AND keyword LIKE '%KEYWORD_QUEST_MASTER_CHAR_7002_0%'
      AND  DEFINITION LIKE '%inv_policy_values.CalcFundAccValue%' ;
      
SELECT * FROM SYSCFG_RULE_KEYWORD_TYPE

SELECT * FROM SYSCFG_RULE_TYPES
SELECT * FROM SYSCFG_RULE_VALUE_BASE    
SELECT * FROM SYSCFG_RULE_SEQUENCE_TYPE
SELECT * FROM SYSCFG_RULE_KEYWORD_TYPE
SELECT * FROM SYSCFG_RULE_KEYWORDS
-- Rule Bus / rb / mapping with PL code
INSIS_GEN_CFG_V10.rb_srv_list
Package 'RB_DATA' 
