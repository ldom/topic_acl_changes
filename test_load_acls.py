import unittest

from acl_external import ExternalACL
from input import load_from_kafka_acl_output


class TestLoadACLs(unittest.TestCase):
    def test_simple(self):
        kafka_acls_output = """
[2021-02-03 15:19:40,797] WARN The configuration 'sasl.jaas.config' was supplied but isn't a known config. (org.apache.kafka.clients.admin.AdminClientConfig)
Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=connect-cluster-status, patternType=LITERAL)`:
 	(principal=User:kafka_connect, host=*, operation=ALL, permissionType=ALLOW)

Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=connect-cluster-, patternType=PREFIXED)`:
 	(principal=User:kafka_connect, host=*, operation=ALL, permissionType=ALLOW)

Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=_confluent-monitoring, patternType=LITERAL)`:
 	(principal=User:control_center, host=*, operation=CREATE, permissionType=ALLOW)
	(principal=User:test2, host=*, operation=DESCRIBE, permissionType=ALLOW)
	(principal=User:test2, host=*, operation=CREATE, permissionType=ALLOW)
	(principal=User:control_center, host=*, operation=READ, permissionType=ALLOW)
	(principal=User:test2, host=*, operation=READ, permissionType=ALLOW)
	(principal=User:control_center, host=*, operation=WRITE, permissionType=ALLOW)
	(principal=User:test2, host=*, operation=DESCRIBE_CONFIGS, permissionType=ALLOW)
	(principal=User:test2, host=*, operation=WRITE, permissionType=ALLOW)
	(principal=User:control_center, host=*, operation=DESCRIBE, permissionType=ALLOW)
	(principal=User:control_center, host=*, operation=DESCRIBE_CONFIGS, permissionType=ALLOW)
        """
        ret = ExternalACL.parse_acl_output(kafka_acls_output)
        self.assertEqual(len(ret), 3)
        self.assertEqual(len(ret[2]['acls']), 10)


    def test_long_output(self):
        pnc_output = """
        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=CUSTOM.Account.AOPAccount, patternType=LITERAL)`: 
         	(principal=User:xqaopkfkusr001, host=*, operation=WRITE, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=dsp-streams-bian-mapper-oly-pref-link-channel-store-changelog, patternType=LITERAL)`: 
         	(principal=User:xqdspkfkusr019, host=*, operation=READ, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr019, host=*, operation=WRITE, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=BIAN.PositionKeeping.PostedTransaction, patternType=LITERAL)`: 
         	(principal=User:xqdspkfkusr036, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr047, host=*, operation=READ, permissionType=ALLOW)
        	(principal=User:xqlcxkfkusr001, host=*, operation=READ, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr040, host=*, operation=WRITE, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=RAW.CIF.LOAD.CIFALK, patternType=LITERAL)`: 
         	(principal=User:xqdspkfkusr010, host=*, operation=READ, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=BIAN.RewardPointsAwardsAndRedemption.Initiation, patternType=LITERAL)`: 
         	(principal=User:xqrewkfkusr001, host=*, operation=READ, permissionType=ALLOW)
        	(principal=User:xqrewkfkusr001, host=*, operation=WRITE, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=dsp-streams-bian-mapper-eds-account-account-from-cor-account-changelog, patternType=LITERAL)`: 
         	(principal=User:xqdspkfkusr053, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr053, host=*, operation=READ, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=mm2-configs.MPCFIS.internal, patternType=LITERAL)`: 
         	(principal=User:xqmpckfkusr001, host=*, operation=DESCRIBE_CONFIGS, permissionType=ALLOW)
        	(principal=User:xqmpckfkusr001, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqmpckfkusr001, host=*, operation=READ, permissionType=ALLOW)
        	(principal=User:xqmpckfkusr001, host=*, operation=CREATE, permissionType=ALLOW)
        	(principal=User:xqmpckfkusr001, host=*, operation=DESCRIBE, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=INGESTED.MDMCntrctPrdctRltnp.MDM, patternType=LITERAL)`: 
         	(principal=User:xqdspkfkusr014, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr013, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr018, host=*, operation=READ, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=dsp-alert-preferences-aggregator-aggregate-account-store-repartition, patternType=LITERAL)`: 
         	(principal=User:xqDMGkfkusr1, host=*, operation=DELETE, permissionType=ALLOW)
        	(principal=User:xqdmgkfkusr001, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:DMG-prod-kfkusr001, host=*, operation=DELETE, permissionType=ALLOW)
        	(principal=User:xqdmgkfkusr001, host=*, operation=READ, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=dsp-streams-bian-mapper-customerreferencedatamanagement-customer-internal-customer-from-mdm-address-changelog, patternType=LITERAL)`: 
         	(principal=User:xqdspkfkusr028, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr028, host=*, operation=READ, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=dsp-streams-custom-mapper-fis-monetarytxnexp-accounts-state-store-changelog, patternType=LITERAL)`: 
         	(principal=User:xqdspkfkusr038, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr038, host=*, operation=READ, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=dsp-streams-custom-mapper-fis-monetarytxnexp-accounts-state-store-repartition, patternType=LITERAL)`: 
         	(principal=User:xqdspkfkusr038, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr038, host=*, operation=DELETE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr038, host=*, operation=READ, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=INGESTED.EventPrefByPrefId.OLY, patternType=LITERAL)`: 
         	(principal=User:xqdspkfkusr019, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr019, host=*, operation=READ, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=RAW.COX.LOAD.CONTROLFILE, patternType=LITERAL)`: 
         	(principal=User:xqdspkfkusr007, host=*, operation=READ, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=dsp-streams-bian-mapper-eds-account-account-from-eds-account-changelog, patternType=LITERAL)`: 
         	(principal=User:xqdspkfkusr053, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr053, host=*, operation=READ, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=dmg-alert-preferences-aggregator-aggregate-account-store-changelog, patternType=LITERAL)`: 
         	(principal=User:xqdmgkfkusr001, host=*, operation=READ, permissionType=ALLOW)
        	(principal=User:xqdmgkfkusr001, host=*, operation=WRITE, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=srm-control.MPCFIS.internal, patternType=LITERAL)`: 
         	(principal=User:xqmpckfkusr001, host=*, operation=DESCRIBE_CONFIGS, permissionType=ALLOW)
        	(principal=User:xqmpckfkusr001, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqmpckfkusr001, host=*, operation=READ, permissionType=ALLOW)
        	(principal=User:xqmpckfkusr001, host=*, operation=CREATE, permissionType=ALLOW)
        	(principal=User:xqmpckfkusr001, host=*, operation=DESCRIBE, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=RAW.Intraday.COS, patternType=LITERAL)`: 
         	(principal=User:xqdspkfkusr016, host=*, operation=READ, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=dsp-streams-bian-mapper-fis-fund-hold-bian-account-store-changelog, patternType=LITERAL)`: 
         	(principal=User:xqdspkfkusr003, host=*, operation=READ, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr003, host=*, operation=WRITE, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=BIAN.Account, patternType=LITERAL)`: 
         	(principal=User:xqdspkfkusr044, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr017, host=*, operation=READ, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr029, host=*, operation=READ, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr019, host=*, operation=READ, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr042, host=*, operation=READ, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr036, host=*, operation=READ, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr038, host=*, operation=READ, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr025, host=*, operation=READ, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr003, host=*, operation=READ, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr002, host=*, operation=READ, permissionType=ALLOW)
        	(principal=User:xqlcxkfkusr001, host=*, operation=READ, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr053, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr024, host=*, operation=READ, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr043, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr039, host=*, operation=READ, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr046, host=*, operation=READ, permissionType=ALLOW)
        	(principal=User:xqdmgkfkusr001, host=*, operation=READ, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr018, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr040, host=*, operation=READ, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=dsp-streams-bian-mapper-customerreferencedatamanagement-customer-mdm-contact-method-address-joiner-store-changelog, patternType=LITERAL)`: 
         	(principal=User:xqdspkfkusr028, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr028, host=*, operation=READ, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=RAW.MDM.LOAD.MDMPARTYKEYS, patternType=LITERAL)`: 
         	(principal=User:xqdspkfkusr006, host=*, operation=READ, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=INGESTED.MonetaryTransactionException.FIS, patternType=LITERAL)`: 
         	(principal=User:xqdspkfkusr037, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr038, host=*, operation=READ, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=dsp-streams-bian-mapper-fis-accountbalance-bian-account-store-changelog, patternType=LITERAL)`: 
         	(principal=User:xqdspkfkusr039, host=*, operation=READ, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr039, host=*, operation=WRITE, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=MPCFIS.heartbeats, patternType=LITERAL)`: 
         	(principal=User:xqmpckfkusr001, host=*, operation=READ, permissionType=ALLOW)
        	(principal=User:xqmpckfkusr001, host=*, operation=DESCRIBE_CONFIGS, permissionType=ALLOW)
        	(principal=User:xqmpckfkusr001, host=*, operation=DESCRIBE, permissionType=ALLOW)
        	(principal=User:xqmpckfkusr001, host=*, operation=WRITE, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=BIAN.PositionKeeping.TransactionDisposition, patternType=LITERAL)`: 
         	(principal=User:xqlcxkfkusr001, host=*, operation=READ, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr029, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr047, host=*, operation=READ, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=RAW.COR.REALTIME.POSTTRANS, patternType=LITERAL)`: 
         	(principal=User:xqdspkfkusr041, host=*, operation=READ, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=INTERNAL.Stage.AccountBalanceEntity, patternType=LITERAL)`: 
         	(principal=User:xqdspkfkusr046, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr046, host=*, operation=READ, permissionType=ALLOW)
        	(principal=User:dsp-connect01, host=*, operation=READ, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=INGESTED.MDMDevice.MDM, patternType=LITERAL)`: 
         	(principal=User:xqccpkfkusr001, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr054, host=*, operation=READ, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr028, host=*, operation=READ, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=BIAN.PaymentOrder, patternType=LITERAL)`: 
         	(principal=User:xqppokfkusr001, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr045, host=*, operation=READ, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=dmg-alert-preferences-aggregator-aggregate-account-store-repartition, patternType=LITERAL)`: 
         	(principal=User:xqDMGkfkusr1, host=*, operation=DELETE, permissionType=ALLOW)
        	(principal=User:xqdmgkfkusr001, host=*, operation=READ, permissionType=ALLOW)
        	(principal=User:xqdmgkfkusr001, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:DMG-prod-kfkusr001, host=*, operation=DELETE, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=dsp-streams-bian-mapper-customerreferencedatamanagement-customer-customer-from-contact-method-changelog, patternType=LITERAL)`: 
         	(principal=User:xqdspkfkusr028, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr028, host=*, operation=READ, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=dsp-streams-bian-mapper-oly-simple-account-store-changelog, patternType=LITERAL)`: 
         	(principal=User:xqdspkfkusr019, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr019, host=*, operation=READ, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=dsp-streams-bian-mapper-cor-posted-transactions-accounts-store-changelog, patternType=LITERAL)`: 
         	(principal=User:xqdspkfkusr036, host=*, operation=READ, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr036, host=*, operation=WRITE, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=INGESTED.FundHold.FIS, patternType=LITERAL)`: 
         	(principal=User:xqdspkfkusr003, host=*, operation=READ, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr037, host=*, operation=WRITE, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=INGESTED.MonetaryTxnRelationship.FIS, patternType=LITERAL)`: 
         	(principal=User:xqdspkfkusr037, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr002, host=*, operation=READ, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=dsp-streams-bian-mapper-cos-pendingtransactions-bian-account-store-repartition, patternType=LITERAL)`: 
         	(principal=User:xqdspkfkusr025, host=*, operation=READ, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr025, host=*, operation=DELETE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr025, host=*, operation=WRITE, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=RAW.MasterRecord.COS, patternType=LITERAL)`: 
         	(principal=User:xqdspkfkusr016, host=*, operation=READ, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=dsp-streams-bian-mapper-cos-availablebalance-bian-account-store-repartition, patternType=LITERAL)`: 
         	(principal=User:xqdspkfkusr017, host=*, operation=READ, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr017, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr017, host=*, operation=DELETE, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=dsp-streams-bian-mapper-oly-raw-event-pref-store-repartition, patternType=LITERAL)`: 
         	(principal=User:xqdspkfkusr019, host=*, operation=READ, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr019, host=*, operation=DELETE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr019, host=*, operation=WRITE, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=dsp-streams-bian-mapper-eds-mdm-customer-eds-customer-store-changelog, patternType=LITERAL)`: 
         	(principal=User:xqdspkfkusr054, host=*, operation=READ, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr054, host=*, operation=WRITE, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=dsp-streams-bian-mapper-fis-monetarytransaction-accounts-collision-detection-store-changelog, patternType=LITERAL)`: 
         	(principal=User:xqdspkfkusr040, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr040, host=*, operation=READ, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=sfp-location-data-management-dsp-KTABLE-AGGREGATE-STATE-STORE-0000000004-repartition, patternType=LITERAL)`: 
         	(principal=User:xqaopkfkusr001, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqaopkfkusr001, host=*, operation=READ, permissionType=ALLOW)
        	(principal=User:xqaopkfkusr001, host=*, operation=DELETE, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=sfp-key-translation-service-dsp-sfp-key-translation-service-dsp-state-rs-repartition, patternType=LITERAL)`: 
         	(principal=User:xqsfpkfkusr001, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqsfpkfkusr001, host=*, operation=DELETE, permissionType=ALLOW)
        	(principal=User:xqsfpkfkusr001, host=*, operation=READ, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=dsp-streams-bian-mapper-fis-monetarytxnrelationship-bian-account-store-repartition, patternType=LITERAL)`: 
         	(principal=User:xqdspkfkusr002, host=*, operation=DELETE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr002, host=*, operation=READ, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr002, host=*, operation=WRITE, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=RAW.OLY.LOAD.CHANNELPREF, patternType=LITERAL)`: 
         	(principal=User:xqdspkfkusr020, host=*, operation=READ, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=dsp-streams-custom-mapper-fis-statementcycle-KSTREAM-PEEK-0000000011-repartition, patternType=LITERAL)`: 
         	(principal=User:xqdspkfkusr042, host=*, operation=DELETE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr042, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr042, host=*, operation=READ, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=INGESTED.DispositionTransaction.COR, patternType=LITERAL)`: 
         	(principal=User:xqdspkfkusr027, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr029, host=*, operation=READ, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=dsp-streams-bian-mapper-oly-pref-master-store-changelog, patternType=LITERAL)`: 
         	(principal=User:xqdspkfkusr019, host=*, operation=READ, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr019, host=*, operation=WRITE, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=INGESTED.MasterRecord.COS, patternType=LITERAL)`: 
         	(principal=User:xqdspkfkusr016, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr017, host=*, operation=READ, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=sfp-key-translation-service-dsp-sfp-key-translation-service-dsp-state-mappings-repartition, patternType=LITERAL)`: 
         	(principal=User:xqsfpkfkusr001, host=*, operation=DELETE, permissionType=ALLOW)
        	(principal=User:xqsfpkfkusr001, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqsfpkfkusr001, host=*, operation=READ, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=dsp-streams-bian-mapper-cor-nonsufficientfunds-simple-bian-account-store-repartition, patternType=LITERAL)`: 
         	(principal=User:xqdspkfkusr024, host=*, operation=READ, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr024, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr024, host=*, operation=DELETE, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=INGESTED.AccountNotes.FIS, patternType=LITERAL)`: 
         	(principal=User:xqdspkfkusr037, host=*, operation=WRITE, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=sfp-key-translation-service-dsp-sfp-key-translation-service-dsp-state-rs-changelog, patternType=LITERAL)`: 
         	(principal=User:xqsfpkfkusr001, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqsfpkfkusr001, host=*, operation=READ, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=dsp-streams-bian-mapper-eds-mdm-customer-customer-from-ingested-eds-customer-changelog, patternType=LITERAL)`: 
         	(principal=User:xqdspkfkusr054, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr054, host=*, operation=READ, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=INTEGRATION.AlertsProfiles.AccountId.DMG, patternType=LITERAL)`: 
         	(principal=User:xqdmgkfkusr001, host=*, operation=READ, permissionType=ALLOW)
        	(principal=User:xqdmgkfkusr001, host=*, operation=WRITE, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=dsp-streams-bian-mapper-customerreferencedatamanagement-customer-mdm-address-store-changelog, patternType=LITERAL)`: 
         	(principal=User:xqdspkfkusr028, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr028, host=*, operation=READ, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=INGESTED.PendingDeposits.COS, patternType=LITERAL)`: 
         	(principal=User:xqdspkfkusr016, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr025, host=*, operation=READ, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=sfp-key-translation-service-dsp-KSTREAM-REDUCE-STATE-STORE-0000000004-repartition, patternType=LITERAL)`: 
         	(principal=User:xqsfpkfkusr001, host=*, operation=READ, permissionType=ALLOW)
        	(principal=User:xqsfpkfkusr001, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqsfpkfkusr001, host=*, operation=DELETE, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=INGESTED.EDSAccount.MDM, patternType=LITERAL)`: 
         	(principal=User:xqdspkfkusr051, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr053, host=*, operation=READ, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=BIAN.CustomerReferenceDataManagement.Customer, patternType=LITERAL)`: 
         	(principal=User:xqdspkfkusr028, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqdmgkfkusr001, host=*, operation=READ, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr048, host=*, operation=READ, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=INGESTED.PrefLinkByPrefId.OLY, patternType=LITERAL)`: 
         	(principal=User:xqdspkfkusr019, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr019, host=*, operation=READ, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=BIAN.RewardPointsAwardsAndRedemption.Notification, patternType=LITERAL)`: 
         	(principal=User:xqrewkfkusr001, host=*, operation=WRITE, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=dsp-streams-bian-mapper-oly-simple-customer-party-keys-history-store-repartition, patternType=LITERAL)`: 
         	(principal=User:xqdspkfkusr019, host=*, operation=READ, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr019, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr019, host=*, operation=DELETE, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=dsp-streams-bian-mapper-cor-account-mdm-cntrct-party-rltnp-store-changelog, patternType=LITERAL)`: 
         	(principal=User:xqdspkfkusr043, host=*, operation=READ, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr043, host=*, operation=WRITE, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=RAW.MDM.LOAD.MDMCNTRCTPRDCTRLTNP, patternType=LITERAL)`: 
         	(principal=User:xqdspkfkusr013, host=*, operation=READ, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=INGESTED.JournalArea.COS, patternType=LITERAL)`: 
         	(principal=User:xqdspkfkusr017, host=*, operation=READ, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr016, host=*, operation=WRITE, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=dsp-streams-bian-mapper-eds-account-balance-produced-state-store-changelog, patternType=LITERAL)`: 
         	(principal=User:xqdspkfkusr053, host=*, operation=READ, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr053, host=*, operation=WRITE, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=CUSTOM.CustomerEventHistory.CustomerModeEvent, patternType=LITERAL)`: 
         	(principal=User:xqdspkfkusr033, host=*, operation=READ, permissionType=ALLOW)
        	(principal=User:xqlcxkfkusr001, host=*, operation=READ, permissionType=ALLOW)
        	(principal=User:xqlcxkfkusr001, host=*, operation=WRITE, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=dsp-streams-bian-mapper-oly-channel-pref-store-changelog, patternType=LITERAL)`: 
         	(principal=User:xqdspkfkusr019, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr019, host=*, operation=READ, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=RAW_OLY_CHANNEL_PREF, patternType=LITERAL)`: 
         	(principal=User:xqdspkfkusr020, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr019, host=*, operation=READ, permissionType=ALLOW)
        	(principal=User:xqolykfkusr001, host=*, operation=WRITE, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=dsp-streams-bian-mapper-oly-pref-link-event-store-changelog, patternType=LITERAL)`: 
         	(principal=User:xqdspkfkusr019, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr019, host=*, operation=READ, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=BIAN.PositionKeeping.TransactionDeposit, patternType=LITERAL)`: 
         	(principal=User:xqdspkfkusr025, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr047, host=*, operation=READ, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=CUSTOM.CustomerAccessEntitlement.AssociationCustomerPreference, patternType=LITERAL)`: 
         	(principal=User:xqccpkfkusr001, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqccpkfkusr001, host=*, operation=READ, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=dsp-streams-bian-mapper-customerreferencedatamanagement-customer-customer-from-mdm-address-changelog, patternType=LITERAL)`: 
         	(principal=User:xqdspkfkusr028, host=*, operation=READ, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr028, host=*, operation=WRITE, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=dsp-streams-bian-mapper-transactionmodality-bian-transactionmodality-aggregation-store-changelog, patternType=LITERAL)`: 
         	(principal=User:xqdspkfkusr034, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr034, host=*, operation=READ, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=dsp-streams-bian-mapper-cor-posted-transactions-accounts-store-repartition, patternType=LITERAL)`: 
         	(principal=User:xqdspkfkusr036, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr036, host=*, operation=READ, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr036, host=*, operation=DELETE, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=dsp-streams-bian-mapper-oly-simple-customer-party-keys-history-store-changelog, patternType=LITERAL)`: 
         	(principal=User:xqdspkfkusr019, host=*, operation=READ, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr019, host=*, operation=WRITE, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=INGESTED.PostedTransaction.COR, patternType=LITERAL)`: 
         	(principal=User:xqdspkfkusr036, host=*, operation=READ, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr041, host=*, operation=WRITE, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=mm2-offsets.MPCFIS.internal, patternType=LITERAL)`: 
         	(principal=User:xqmpckfkusr001, host=*, operation=DESCRIBE_CONFIGS, permissionType=ALLOW)
        	(principal=User:xqmpckfkusr001, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqmpckfkusr001, host=*, operation=READ, permissionType=ALLOW)
        	(principal=User:xqmpckfkusr001, host=*, operation=CREATE, permissionType=ALLOW)
        	(principal=User:xqmpckfkusr001, host=*, operation=DESCRIBE, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=BIAN.Correspondence.Notification, patternType=LITERAL)`: 
         	(principal=User:xqdmgkfkusr001, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqdmgkfkusr001, host=*, operation=READ, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=INTEGRATION.CustomerPartyKeys.MDM, patternType=LITERAL)`: 
         	(principal=User:xqdspkfkusr008, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:CMT-prod-kfkusr001, host=*, operation=READ, permissionType=ALLOW)
        	(principal=User:xqCMTkfkusr1, host=*, operation=READ, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=RAW.COR.LOAD.POSTTRANS, patternType=LITERAL)`: 
         	(principal=User:xqdspkfkusr041, host=*, operation=READ, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=INGESTED.MDMContactMethod.MDM, patternType=LITERAL)`: 
         	(principal=User:xqdspkfkusr028, host=*, operation=READ, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr004, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr026, host=*, operation=WRITE, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=sfp-key-translation-service-dsp-KSTREAM-REDUCE-STATE-STORE-0000000013-repartition, patternType=LITERAL)`: 
         	(principal=User:xqsfpkfkusr001, host=*, operation=READ, permissionType=ALLOW)
        	(principal=User:xqsfpkfkusr001, host=*, operation=DELETE, permissionType=ALLOW)
        	(principal=User:xqsfpkfkusr001, host=*, operation=WRITE, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=dsp-streams-bian-mapper-oly-KSTREAM-TRANSFORM-0000000030-repartition, patternType=LITERAL)`: 
         	(principal=User:xqdspkfkusr019, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr019, host=*, operation=DELETE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr019, host=*, operation=READ, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=dsp-streams-bian-mapper-eds-mdm-customer-internal-customer-from-ingested-mdm-device-changelog, patternType=LITERAL)`: 
         	(principal=User:xqdspkfkusr054, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr054, host=*, operation=READ, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=RAW.MPX.LOAD.TRANCODE, patternType=LITERAL)`: 
         	(principal=User:xqdspkfkusr035, host=*, operation=READ, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=dsp-streams-bian-mapper-cos-pendingtransactions-bian-account-store-changelog, patternType=LITERAL)`: 
         	(principal=User:xqdspkfkusr025, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr025, host=*, operation=READ, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=CUSTOM.LocationDataManagement.BranchDirectory.ByBranchTypeAndDivision, patternType=LITERAL)`: 
         	(principal=User:xqaopkfkusr001, host=*, operation=READ, permissionType=ALLOW)
        	(principal=User:xqaopkfkusr001, host=*, operation=WRITE, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=GROUP, name=srm-service, patternType=LITERAL)`: 
         	(principal=User:xqmpckfkusr001, host=*, operation=DESCRIBE, permissionType=ALLOW)
        	(principal=User:xqmpckfkusr001, host=*, operation=READ, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=dsp-streams-custom-mapper-fis-statementcycle-bian-account-store-changelog, patternType=LITERAL)`: 
         	(principal=User:xqdspkfkusr042, host=*, operation=READ, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr042, host=*, operation=WRITE, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=CUSTOM.CustomerReferenceDataManagement.AOPParty, patternType=LITERAL)`: 
         	(principal=User:xqaopkfkusr001, host=*, operation=WRITE, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=dsp-streams-bian-mapper-cor-account-mdm-cntrct-party-rltnp-store-repartition, patternType=LITERAL)`: 
         	(principal=User:xqdspkfkusr043, host=*, operation=READ, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr043, host=*, operation=DELETE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr043, host=*, operation=WRITE, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=RAW_OLY_EVENT_PREF, patternType=LITERAL)`: 
         	(principal=User:xqolykfkusr001, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr021, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr019, host=*, operation=READ, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=INGESTED.MDMAddress.MDM, patternType=LITERAL)`: 
         	(principal=User:xqdspkfkusr031, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr028, host=*, operation=READ, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr026, host=*, operation=WRITE, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=BIAN.Account.AccountModality, patternType=LITERAL)`: 
         	(principal=User:dsp-connect01, host=*, operation=READ, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr032, host=*, operation=WRITE, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=MPCFIS.checkpoints.internal, patternType=LITERAL)`: 
         	(principal=User:xqmpckfkusr001, host=*, operation=DESCRIBE_CONFIGS, permissionType=ALLOW)
        	(principal=User:xqmpckfkusr001, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqmpckfkusr001, host=*, operation=READ, permissionType=ALLOW)
        	(principal=User:xqmpckfkusr001, host=*, operation=CREATE, permissionType=ALLOW)
        	(principal=User:xqmpckfkusr001, host=*, operation=DESCRIBE, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=dsp-streams-bian-mapper-fis-account-casa-open-account-state-store-repartition, patternType=LITERAL)`: 
         	(principal=User:xqdspkfkusr044, host=*, operation=DELETE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr044, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr044, host=*, operation=READ, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=BIAN.PositionKeeping.TransactionHold, patternType=LITERAL)`: 
         	(principal=User:xqlcxkfkusr001, host=*, operation=READ, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr025, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr003, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr047, host=*, operation=READ, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=dsp-streams-bian-mapper-customerreferencedatamanagement-customer-mdm-device-store-changelog, patternType=LITERAL)`: 
         	(principal=User:xqdspkfkusr028, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr028, host=*, operation=READ, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=dsp-streams-bian-mapper-eds-account-account-from-casa-account-changelog, patternType=LITERAL)`: 
         	(principal=User:xqdspkfkusr053, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr053, host=*, operation=READ, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=dsp-streams-bian-mapper-fis-account-mdm-cntrct-party-rltnp-state-store-changelog, patternType=LITERAL)`: 
         	(principal=User:xqdspkfkusr044, host=*, operation=READ, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr044, host=*, operation=WRITE, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=dsp-streams-bian-mapper-oly-raw-event-pref-store-changelog, patternType=LITERAL)`: 
         	(principal=User:xqdspkfkusr019, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr019, host=*, operation=READ, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=dsp-streams-bian-mapper-oly-INGESTED.PrefLinkByPrefId.OLY-STATE-STORE-0000000037-changelog, patternType=LITERAL)`: 
         	(principal=User:xqdspkfkusr019, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr019, host=*, operation=READ, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=dsp-streams-bian-mapper-cor-account-balance-produced-state-store-changelog, patternType=LITERAL)`: 
         	(principal=User:xqdspkfkusr043, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr043, host=*, operation=READ, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=dsp-streams-bian-mapper-fis-monetarytxnrelationship-KSTREAM-PEEK-0000000012-repartition, patternType=LITERAL)`: 
         	(principal=User:xqdspkfkusr002, host=*, operation=READ, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr002, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr002, host=*, operation=DELETE, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=BIAN.RewardPointsAccount.Enrollment, patternType=LITERAL)`: 
         	(principal=User:xqrewkfkusr001, host=*, operation=READ, permissionType=ALLOW)
        	(principal=User:xqrewkfkusr001, host=*, operation=WRITE, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=dmg-alert-trigger-low-balance-balances-data-state-store-changelog, patternType=LITERAL)`: 
         	(principal=User:xqdmgkfkusr001, host=*, operation=READ, permissionType=ALLOW)
        	(principal=User:xqdmgkfkusr001, host=*, operation=WRITE, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=CUSTOM.CustomerAccessEntitlement.CustomerPreference, patternType=LITERAL)`: 
         	(principal=User:xqdspkfkusr019, host=*, operation=READ, permissionType=ALLOW)
        	(principal=User:xqlcxkfkusr001, host=*, operation=READ, permissionType=ALLOW)
        	(principal=User:xqccpkfkusr001, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqdmgkfkusr001, host=*, operation=READ, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr019, host=*, operation=WRITE, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=INGESTED.MDMPartyName.MDM, patternType=LITERAL)`: 
         	(principal=User:xqdspkfkusr028, host=*, operation=READ, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr050, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr026, host=*, operation=WRITE, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=srm-metrics.MPCFIS.internal, patternType=LITERAL)`: 
         	(principal=User:xqmpckfkusr001, host=*, operation=DESCRIBE_CONFIGS, permissionType=ALLOW)
        	(principal=User:xqmpckfkusr001, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqmpckfkusr001, host=*, operation=READ, permissionType=ALLOW)
        	(principal=User:xqmpckfkusr001, host=*, operation=CREATE, permissionType=ALLOW)
        	(principal=User:xqmpckfkusr001, host=*, operation=DESCRIBE, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=dsp-streams-bian-mapper-fis-monetarytxnrelationship-bian-account-store-changelog, patternType=LITERAL)`: 
         	(principal=User:xqdspkfkusr002, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr002, host=*, operation=READ, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=INTERNAL.Error.DSP, patternType=LITERAL)`: 
         	(principal=User:xqdspkfkusr027, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr032, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr044, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr056, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr001, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr037, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr040, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr049, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr011, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr033, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr003, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr042, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr022, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr034, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr035, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr014, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr052, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr045, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr002, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr006, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr004, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr038, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr024, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr055, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr007, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr030, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr050, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr039, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr031, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr026, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr023, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr025, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr010, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr053, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqdmgkfkusr001, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr005, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr009, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr047, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr013, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr043, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr012, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr041, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr020, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr048, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr051, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr017, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr015, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr028, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr021, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr018, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr046, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr036, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr054, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr019, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr008, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr029, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr016, host=*, operation=WRITE, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=dsp-streams-bian-mapper-customerreferencedatamanagement-customer-internal-customer-from-party-name-changelog, patternType=LITERAL)`: 
         	(principal=User:xqdspkfkusr028, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr028, host=*, operation=READ, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=GROUP, name=MPCFIS-mm2, patternType=LITERAL)`: 
         	(principal=User:xqmpckfkusr001, host=*, operation=DESCRIBE, permissionType=ALLOW)
        	(principal=User:xqmpckfkusr001, host=*, operation=READ, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=CUSTOM.PaymentException, patternType=LITERAL)`: 
         	(principal=User:xqdspkfkusr038, host=*, operation=WRITE, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=dsp-streams-bian-mapper-oly-simple-account-store-repartition, patternType=LITERAL)`: 
         	(principal=User:xqdspkfkusr019, host=*, operation=READ, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr019, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr019, host=*, operation=DELETE, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=dsp-streams-bian-mapper-eds-account-account-from-casa-account-repartition, patternType=LITERAL)`: 
         	(principal=User:xqdspkfkusr053, host=*, operation=READ, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr053, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr053, host=*, operation=DELETE, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=CUSTOM.CustomerPartyKeysHistory.KTS, patternType=LITERAL)`: 
         	(principal=User:xqCMTkfkusr1, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:CMT-prod-kfkusr001, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr019, host=*, operation=READ, permissionType=ALLOW)
        	(principal=User:xqsfpkfkusr001, host=*, operation=READ, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=sfp-key-translation-service-dsp-KSTREAM-REDUCE-STATE-STORE-0000000013-changelog, patternType=LITERAL)`: 
         	(principal=User:xqsfpkfkusr001, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqsfpkfkusr001, host=*, operation=READ, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=dsp-streams-bian-mapper-oly-KSTREAM-KEY-SELECT-0000000055-repartition, patternType=LITERAL)`: 
         	(principal=User:xqdspkfkusr019, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr019, host=*, operation=READ, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr019, host=*, operation=DELETE, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=dsp-streams-bian-mapper-cor-disptrans-bian-account-store-changelog, patternType=LITERAL)`: 
         	(principal=User:xqdspkfkusr029, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr029, host=*, operation=READ, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=INTERNAL.Error.Connect, patternType=LITERAL)`: 
         	(principal=User:dsp-connect01, host=*, operation=WRITE, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=RAW.OLY.LOAD.PREFMASTER, patternType=LITERAL)`: 
         	(principal=User:xqdspkfkusr023, host=*, operation=READ, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=dsp-streams-bian-mapper-customerreferencedatamanagement-customer-customer-from-party-name-changelog, patternType=LITERAL)`: 
         	(principal=User:xqdspkfkusr028, host=*, operation=READ, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr028, host=*, operation=WRITE, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=RAW_OLY_PREF_LINK, patternType=LITERAL)`: 
         	(principal=User:xqdspkfkusr019, host=*, operation=READ, permissionType=ALLOW)
        	(principal=User:xqolykfkusr001, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr022, host=*, operation=WRITE, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=BIAN.CustomerReferenceDataManagement.EDS, patternType=LITERAL)`: 
         	(principal=User:xqdspkfkusr054, host=*, operation=WRITE, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=RAW.CIFKeys.CIF, patternType=LITERAL)`: 
         	(principal=User:xqdspkfkusr009, host=*, operation=READ, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=dsp-streams-bian-mapper-fis-fund-hold-bian-account-store-repartition, patternType=LITERAL)`: 
         	(principal=User:xqdspkfkusr003, host=*, operation=READ, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr003, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr003, host=*, operation=DELETE, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=dsp-streams-custom-mapper-fis-monetarytxnrelationship-KSTREAM-PEEK-0000000012-repartition, patternType=LITERAL)`: 
         	(principal=User:xqdspkfkusr002, host=*, operation=READ, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr002, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr002, host=*, operation=DELETE, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=INTEGRATION.NotificationsMQ.DMG, patternType=LITERAL)`: 
         	(principal=User:xqdmgkfkusr001, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqdmgkfkusr001, host=*, operation=READ, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=dsp-streams-bian-mapper-customerreferencedatamanagement-customer-contact-method-store-changelog, patternType=LITERAL)`: 
         	(principal=User:xqdspkfkusr028, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr028, host=*, operation=READ, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=BIAN.PositionKeeping.TransactionModality, patternType=LITERAL)`: 
         	(principal=User:xqdspkfkusr034, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:dsp-connect01, host=*, operation=READ, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=INGESTED.MDMContract.MDM, patternType=LITERAL)`: 
         	(principal=User:xqdspkfkusr011, host=*, operation=WRITE, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=dsp-streams-bian-mapper-fis-account-casa-open-account-state-store-changelog, patternType=LITERAL)`: 
         	(principal=User:xqdspkfkusr044, host=*, operation=READ, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr044, host=*, operation=WRITE, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=RAW.MDM.LOAD.MDMCNTCTMETHOD, patternType=LITERAL)`: 
         	(principal=User:xqdspkfkusr004, host=*, operation=READ, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=dsp-streams-bian-mapper-fis-monetarytransaction-accounts-collision-detection-store-repartition, patternType=LITERAL)`: 
         	(principal=User:xqdspkfkusr040, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr040, host=*, operation=DELETE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr040, host=*, operation=READ, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=RAW.COR.REALTIME.MASTER, patternType=LITERAL)`: 
         	(principal=User:xqdspkfkusr030, host=*, operation=READ, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=BIAN.ServicingOrder.ScheduleInstruction, patternType=LITERAL)`: 
         	(principal=User:xqdspkfkusr057, host=*, operation=READ, permissionType=ALLOW)
        	(principal=User:xqppokfkusr001, host=*, operation=WRITE, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=INGESTED.PrefLinkByChannelPrefId.OLY, patternType=LITERAL)`: 
         	(principal=User:xqdspkfkusr019, host=*, operation=READ, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr019, host=*, operation=WRITE, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=srm-service-topic-metrics-minutes-store-changelog, patternType=LITERAL)`: 
         	(principal=User:xqmpckfkusr001, host=*, operation=DESCRIBE_CONFIGS, permissionType=ALLOW)
        	(principal=User:xqmpckfkusr001, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqmpckfkusr001, host=*, operation=READ, permissionType=ALLOW)
        	(principal=User:xqmpckfkusr001, host=*, operation=CREATE, permissionType=ALLOW)
        	(principal=User:xqmpckfkusr001, host=*, operation=DESCRIBE, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=dmg-alert-trigger-low-balance-alert-profiles-data-state-store-changelog, patternType=LITERAL)`: 
         	(principal=User:xqdmgkfkusr001, host=*, operation=READ, permissionType=ALLOW)
        	(principal=User:xqdmgkfkusr001, host=*, operation=WRITE, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=dsp-streams-bian-mapper-cor-nonsufficientfunds-cor-nsf-state-store-repartition, patternType=LITERAL)`: 
         	(principal=User:xqdspkfkusr024, host=*, operation=READ, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr024, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr024, host=*, operation=DELETE, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=sfp-key-translation-service-dsp-sfp-key-translation-service-dsp-state-mappings-changelog, patternType=LITERAL)`: 
         	(principal=User:xqsfpkfkusr001, host=*, operation=READ, permissionType=ALLOW)
        	(principal=User:xqsfpkfkusr001, host=*, operation=WRITE, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=RAW.CIF.LOAD.CIFPERM, patternType=LITERAL)`: 
         	(principal=User:xqdspkfkusr010, host=*, operation=READ, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=CUSTOM.Model.AlertConfiguration, patternType=LITERAL)`: 
         	(principal=User:xqdmgkfkusr001, host=*, operation=WRITE, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=RAW.MPX.LOAD.STATEMENTCYCLE, patternType=LITERAL)`: 
         	(principal=User:xqdspkfkusr042, host=*, operation=READ, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=dsp-streams-bian-mapper-customerreferencedatamanagement-customer-mdm-party-name-and-device-joiner-store-changelog, patternType=LITERAL)`: 
         	(principal=User:xqdspkfkusr028, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr028, host=*, operation=READ, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=RAW.MDM.LOAD.MDMPARTY, patternType=LITERAL)`: 
         	(principal=User:xqdspkfkusr005, host=*, operation=READ, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=CUSTOM.Account.NonSufficientFunds, patternType=LITERAL)`: 
         	(principal=User:xqlcxkfkusr001, host=*, operation=READ, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr046, host=*, operation=READ, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr024, host=*, operation=WRITE, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=RAW.MDM.REALTIME.DATA, patternType=LITERAL)`: 
         	(principal=User:xqdspkfkusr026, host=*, operation=READ, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr015, host=*, operation=READ, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr014, host=*, operation=READ, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=dsp-streams-bian-mapper-customerreferencedatamanagement-customer-internal-customer-from-contact-method-changelog, patternType=LITERAL)`: 
         	(principal=User:xqdspkfkusr028, host=*, operation=READ, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr028, host=*, operation=WRITE, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=BIAN.LocationDataManagement.BranchDirectory, patternType=LITERAL)`: 
         	(principal=User:xqaopkfkusr001, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqsfpkfkusr001, host=*, operation=READ, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=RAW.MDM.LOAD.MDMCNTRCTPRTYADDRESS, patternType=LITERAL)`: 
         	(principal=User:xqdspkfkusr037, host=*, operation=READ, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=dsp-streams-custom-mapper-fis-monetarytxnrelationship-bian-account-store-repartition, patternType=LITERAL)`: 
         	(principal=User:xqdspkfkusr002, host=*, operation=READ, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr002, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr002, host=*, operation=DELETE, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=dsp-streams-bian-mapper-eds-account-account-from-cor-account-repartition, patternType=LITERAL)`: 
         	(principal=User:xqdspkfkusr053, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr053, host=*, operation=DELETE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr053, host=*, operation=READ, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=INGESTED.CasaOpenAccount.FIS, patternType=LITERAL)`: 
         	(principal=User:xqdspkfkusr053, host=*, operation=READ, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr037, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr044, host=*, operation=READ, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=RAW.OLY.LOAD.EVENTPREF, patternType=LITERAL)`: 
         	(principal=User:xqdspkfkusr021, host=*, operation=READ, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=INGESTED.MDMCntrctPartyAddress.MDM, patternType=LITERAL)`: 
         	(principal=User:xqdspkfkusr001, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr026, host=*, operation=WRITE, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=dsp-streams-bian-mapper-eds-mdm-customer-mdmdevice-store-changelog, patternType=LITERAL)`: 
         	(principal=User:xqdspkfkusr054, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr054, host=*, operation=READ, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=RAW, patternType=PREFIXED)`: 
         	(principal=User:dsp-connect01, host=*, operation=WRITE, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=INGESTED.MonetaryTransaction.FIS, patternType=LITERAL)`: 
         	(principal=User:xqdspkfkusr040, host=*, operation=READ, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr037, host=*, operation=WRITE, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=INGESTED.AccountBalanceChange.FIS, patternType=LITERAL)`: 
         	(principal=User:xqdspkfkusr037, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr039, host=*, operation=READ, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=INTERNAL.CIF.KEY.HASH, patternType=LITERAL)`: 
         	(principal=User:xqdspkfkusr009, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr010, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr010, host=*, operation=READ, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr009, host=*, operation=READ, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=BIAN.DocumentServices.DocumentManagement, patternType=LITERAL)`: 
         	(principal=User:xqedckfkusr001, host=*, operation=WRITE, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=dsp-streams-bian-mapper-cor-disptrans-bian-account-store-repartition, patternType=LITERAL)`: 
         	(principal=User:xqdspkfkusr029, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr029, host=*, operation=DELETE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr029, host=*, operation=READ, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=dsp-streams-bian-mapper-oly-raw-channel-pref-store-repartition, patternType=LITERAL)`: 
         	(principal=User:xqdspkfkusr019, host=*, operation=READ, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr019, host=*, operation=DELETE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr019, host=*, operation=WRITE, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=RAW.MDM.LOAD.MDMCONTRACT, patternType=LITERAL)`: 
         	(principal=User:xqdspkfkusr011, host=*, operation=READ, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=INGESTED.EDSParty.MDM, patternType=LITERAL)`: 
         	(principal=User:xqdspkfkusr052, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr054, host=*, operation=READ, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=dsp-streams-bian-mapper-oly-event-pref-store-changelog, patternType=LITERAL)`: 
         	(principal=User:xqdspkfkusr019, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr019, host=*, operation=READ, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=RAW.MDM.LOAD.MDMPARTYNAME, patternType=LITERAL)`: 
         	(principal=User:xqdspkfkusr050, host=*, operation=READ, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=sfp-location-data-management-dsp-BIAN.LocationDataManagement.BranchDirectory-STATE-STORE-0000000000-changelog, patternType=LITERAL)`: 
         	(principal=User:xqaopkfkusr001, host=*, operation=READ, permissionType=ALLOW)
        	(principal=User:xqaopkfkusr001, host=*, operation=WRITE, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=INGESTED.ChannelPrefByPrefId.OLY, patternType=LITERAL)`: 
         	(principal=User:xqdspkfkusr019, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr019, host=*, operation=READ, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=dsp-streams-bian-mapper-fis-account-mdm-cntrct-party-rltnp-state-store-repartition, patternType=LITERAL)`: 
         	(principal=User:xqdspkfkusr044, host=*, operation=DELETE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr044, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr044, host=*, operation=READ, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=BIAN.Correspondence.EventPublication, patternType=LITERAL)`: 
         	(principal=User:xqedckfkusr001, host=*, operation=READ, permissionType=ALLOW)
        	(principal=User:xqwcikfkusr002, host=*, operation=WRITE, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=RAW.JournalRecord.COS, patternType=LITERAL)`: 
         	(principal=User:xqdspkfkusr016, host=*, operation=READ, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=BIAN.PaymentExecution, patternType=LITERAL)`: 
         	(principal=User:xqppokfkusr001, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr045, host=*, operation=READ, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=srm-service-cluster-metrics-minutes-store-changelog, patternType=LITERAL)`: 
         	(principal=User:xqmpckfkusr001, host=*, operation=DESCRIBE_CONFIGS, permissionType=ALLOW)
        	(principal=User:xqmpckfkusr001, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqmpckfkusr001, host=*, operation=READ, permissionType=ALLOW)
        	(principal=User:xqmpckfkusr001, host=*, operation=CREATE, permissionType=ALLOW)
        	(principal=User:xqmpckfkusr001, host=*, operation=DESCRIBE, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=INGESTED.PendingDebits.COS, patternType=LITERAL)`: 
         	(principal=User:xqdspkfkusr016, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr025, host=*, operation=READ, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=dsp-streams-bian-mapper-oly-raw-channel-pref-store-changelog, patternType=LITERAL)`: 
         	(principal=User:xqdspkfkusr019, host=*, operation=READ, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr019, host=*, operation=WRITE, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=CUSTOM.Account.AccountModeEvent, patternType=LITERAL)`: 
         	(principal=User:xqdspkfkusr032, host=*, operation=READ, permissionType=ALLOW)
        	(principal=User:xqlcxkfkusr001, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqdmgkfkusr001, host=*, operation=READ, permissionType=ALLOW)
        	(principal=User:xqlcxkfkusr001, host=*, operation=READ, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=INGESTED.MDMPartyKeys.MDM, patternType=LITERAL)`: 
         	(principal=User:xqdspkfkusr008, host=*, operation=READ, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr015, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr006, host=*, operation=WRITE, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=mm2-status.MPCFIS.internal, patternType=LITERAL)`: 
         	(principal=User:xqmpckfkusr001, host=*, operation=DESCRIBE_CONFIGS, permissionType=ALLOW)
        	(principal=User:xqmpckfkusr001, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqmpckfkusr001, host=*, operation=READ, permissionType=ALLOW)
        	(principal=User:xqmpckfkusr001, host=*, operation=CREATE, permissionType=ALLOW)
        	(principal=User:xqmpckfkusr001, host=*, operation=DESCRIBE, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=dsp-streams-bian-mapper-fis-accountbalance-bian-account-store-repartition, patternType=LITERAL)`: 
         	(principal=User:xqdspkfkusr039, host=*, operation=READ, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr039, host=*, operation=DELETE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr039, host=*, operation=WRITE, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=dsp-streams-custom-mapper-fis-monetarytxnrelationship-bian-account-store-changelog, patternType=LITERAL)`: 
         	(principal=User:xqdspkfkusr002, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr002, host=*, operation=READ, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=INGESTED.MDMParty.MDM, patternType=LITERAL)`: 
         	(principal=User:xqdspkfkusr015, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr005, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr008, host=*, operation=READ, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=RAW_OLY_PREF_MASTER, patternType=LITERAL)`: 
         	(principal=User:xqdspkfkusr023, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr019, host=*, operation=READ, permissionType=ALLOW)
        	(principal=User:xqolykfkusr001, host=*, operation=WRITE, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=RAW.MDM.LOAD.MDMCNTRCTPARTYRLTNP, patternType=LITERAL)`: 
         	(principal=User:xqdspkfkusr012, host=*, operation=READ, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=dsp-streams-bian-mapper-accountmodality-bian-accountmodality-aggregation-store-changelog, patternType=LITERAL)`: 
         	(principal=User:xqdspkfkusr032, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr032, host=*, operation=READ, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=INGESTED.AccountRoles.FIS, patternType=LITERAL)`: 
         	(principal=User:xqdspkfkusr037, host=*, operation=WRITE, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=CUSTOM.CustomerEventHistory.CustomerModality, patternType=LITERAL)`: 
         	(principal=User:xqdspkfkusr033, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:dsp-connect01, host=*, operation=READ, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=CUSTOM.Account.AccountControl, patternType=LITERAL)`: 
         	(principal=User:xqdspkfkusr042, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqedckfkusr001, host=*, operation=READ, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=BIAN.CustomerAccessEntitlement.CustomerAccessProfile, patternType=LITERAL)`: 
         	(principal=User:xqdspkfkusr019, host=*, operation=WRITE, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=srm-service-cluster-metrics-minutes-store-repartition, patternType=LITERAL)`: 
         	(principal=User:xqmpckfkusr001, host=*, operation=DESCRIBE_CONFIGS, permissionType=ALLOW)
        	(principal=User:xqmpckfkusr001, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqmpckfkusr001, host=*, operation=DELETE, permissionType=ALLOW)
        	(principal=User:xqmpckfkusr001, host=*, operation=READ, permissionType=ALLOW)
        	(principal=User:xqmpckfkusr001, host=*, operation=CREATE, permissionType=ALLOW)
        	(principal=User:xqmpckfkusr001, host=*, operation=DESCRIBE, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=BIAN.PositionKeeping.Balance, patternType=LITERAL)`: 
         	(principal=User:xqdspkfkusr044, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr040, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr047, host=*, operation=READ, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr003, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqlcxkfkusr001, host=*, operation=READ, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr039, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr053, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr043, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr017, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr046, host=*, operation=READ, permissionType=ALLOW)
        	(principal=User:xqdmgkfkusr001, host=*, operation=READ, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=dsp-streams-bian-mapper-oly-KSTREAM-TRANSFORM-0000000061-repartition, patternType=LITERAL)`: 
         	(principal=User:xqdspkfkusr019, host=*, operation=READ, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr019, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr019, host=*, operation=DELETE, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=dsp-streams-bian-mapper-customerreferencedatamanagement-customer-customer-from-mdm-device-changelog, patternType=LITERAL)`: 
         	(principal=User:xqdspkfkusr028, host=*, operation=READ, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr028, host=*, operation=WRITE, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=dsp-streams-bian-mapper-cor-nonsufficientfunds-cor-nsf-state-store-changelog, patternType=LITERAL)`: 
         	(principal=User:xqdspkfkusr024, host=*, operation=READ, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr024, host=*, operation=WRITE, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=INGESTED.MasterRecord.COR, patternType=LITERAL)`: 
         	(principal=User:xqdspkfkusr053, host=*, operation=READ, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr043, host=*, operation=READ, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr030, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr024, host=*, operation=READ, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=RAW.OLY.LOAD.PREFLINK, patternType=LITERAL)`: 
         	(principal=User:xqdspkfkusr022, host=*, operation=READ, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=dsp-streams-bian-mapper-customerreferencedatamanagement-customer-internal-customer-from-mdm-device-changelog, patternType=LITERAL)`: 
         	(principal=User:xqdspkfkusr028, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr028, host=*, operation=READ, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=INGESTED.MDMCntrctPartyRltnp.MDM, patternType=LITERAL)`: 
         	(principal=User:xqdspkfkusr043, host=*, operation=READ, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr044, host=*, operation=READ, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr015, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr012, host=*, operation=WRITE, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=dsp-streams-bian-mapper-oly-KSTREAM-KEY-SELECT-0000000066-repartition, patternType=LITERAL)`: 
         	(principal=User:xqdspkfkusr019, host=*, operation=READ, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr019, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr019, host=*, operation=DELETE, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=INGESTED.PrefLinkByEventPrefId.OLY, patternType=LITERAL)`: 
         	(principal=User:xqdspkfkusr019, host=*, operation=READ, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr019, host=*, operation=WRITE, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=dsp-streams-bian-mapper-eds-mdm-customer-customer-from-ingested-mdm-device-changelog, patternType=LITERAL)`: 
         	(principal=User:xqdspkfkusr054, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr054, host=*, operation=READ, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=dsp-streams-bian-mapper-customerreferencedatamanagement-customer-mdm-party-name-store-changelog, patternType=LITERAL)`: 
         	(principal=User:xqdspkfkusr028, host=*, operation=READ, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr028, host=*, operation=WRITE, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=CUSTOM.Account.EndOfDayRunInfo, patternType=LITERAL)`: 
         	(principal=User:dsp-connect01, host=*, operation=READ, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr047, host=*, operation=READ, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr007, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqlcxkfkusr001, host=*, operation=READ, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=MPCFIS.retail_deposits, patternType=LITERAL)`: 
         	(principal=User:xqmpckfkusr001, host=*, operation=DESCRIBE_CONFIGS, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr037, host=*, operation=READ, permissionType=ALLOW)
        	(principal=User:xqmpckfkusr001, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqmpckfkusr001, host=*, operation=READ, permissionType=ALLOW)
        	(principal=User:xqmpckfkusr001, host=*, operation=DESCRIBE, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=dsp-alert-preferences-aggregator-aggregate-account-store-changelog, patternType=LITERAL)`: 
         	(principal=User:xqdmgkfkusr001, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqdmgkfkusr001, host=*, operation=READ, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=dsp-streams-bian-mapper-cor-account-cor-account-state-store-changelog, patternType=LITERAL)`: 
         	(principal=User:xqdspkfkusr043, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr043, host=*, operation=READ, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=RAW.MDM.LOAD.MDMADDR, patternType=LITERAL)`: 
         	(principal=User:xqdspkfkusr031, host=*, operation=READ, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=sfp-location-data-management-dsp-KTABLE-AGGREGATE-STATE-STORE-0000000004-changelog, patternType=LITERAL)`: 
         	(principal=User:xqaopkfkusr001, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqaopkfkusr001, host=*, operation=READ, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=dsp-streams-bian-mapper-eds-account-account-from-eds-account-repartition, patternType=LITERAL)`: 
         	(principal=User:xqdspkfkusr053, host=*, operation=READ, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr053, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr053, host=*, operation=DELETE, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=dsp-account-summary-balance-stream-state-store-changelog, patternType=LITERAL)`: 
         	(principal=User:xqdspkfkusr046, host=*, operation=READ, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr046, host=*, operation=WRITE, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=CUSTOM.PositionKeeping.TransactionModeEvent, patternType=LITERAL)`: 
         	(principal=User:xqdmgkfkusr001, host=*, operation=READ, permissionType=ALLOW)
        	(principal=User:xqlcxkfkusr001, host=*, operation=READ, permissionType=ALLOW)
        	(principal=User:xqlcxkfkusr001, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr034, host=*, operation=READ, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=dsp-streams-bian-mapper-customermodality-custom-customermodality-aggregation-store-changelog, patternType=LITERAL)`: 
         	(principal=User:xqdspkfkusr033, host=*, operation=READ, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr033, host=*, operation=WRITE, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=srm-service-topic-metrics-minutes-store-repartition, patternType=LITERAL)`: 
         	(principal=User:xqmpckfkusr001, host=*, operation=DESCRIBE_CONFIGS, permissionType=ALLOW)
        	(principal=User:xqmpckfkusr001, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqmpckfkusr001, host=*, operation=DELETE, permissionType=ALLOW)
        	(principal=User:xqmpckfkusr001, host=*, operation=READ, permissionType=ALLOW)
        	(principal=User:xqmpckfkusr001, host=*, operation=CREATE, permissionType=ALLOW)
        	(principal=User:xqmpckfkusr001, host=*, operation=DESCRIBE, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=dsp-streams-custom-mapper-fis-statementcycle-bian-account-store-repartition, patternType=LITERAL)`: 
         	(principal=User:xqdspkfkusr042, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr042, host=*, operation=DELETE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr042, host=*, operation=READ, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=RAW.COR.REALTIME.DISPTRANS, patternType=LITERAL)`: 
         	(principal=User:xqdspkfkusr027, host=*, operation=READ, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=RAW.COR.LOAD.DISPTRANS, patternType=LITERAL)`: 
         	(principal=User:xqdspkfkusr027, host=*, operation=READ, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=dsp-streams-bian-mapper-mdm-product-code-banking-product-aggregation-store-changelog, patternType=LITERAL)`: 
         	(principal=User:xqdspkfkusr018, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr018, host=*, operation=READ, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=heartbeats, patternType=LITERAL)`: 
         	(principal=User:xqmpckfkusr001, host=*, operation=DESCRIBE_CONFIGS, permissionType=ALLOW)
        	(principal=User:xqmpckfkusr001, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqmpckfkusr001, host=*, operation=READ, permissionType=ALLOW)
        	(principal=User:xqmpckfkusr001, host=*, operation=CREATE, permissionType=ALLOW)
        	(principal=User:xqmpckfkusr001, host=*, operation=DESCRIBE, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=RAW.COR.LOAD.MASTER, patternType=LITERAL)`: 
         	(principal=User:xqdspkfkusr030, host=*, operation=READ, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=dsp-streams-bian-mapper-cos-availablebalance-bian-account-store-changelog, patternType=LITERAL)`: 
         	(principal=User:xqdspkfkusr017, host=*, operation=READ, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr017, host=*, operation=WRITE, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=dsp-streams-bian-mapper-cor-nonsufficientfunds-simple-bian-account-store-changelog, patternType=LITERAL)`: 
         	(principal=User:xqdspkfkusr024, host=*, operation=READ, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr024, host=*, operation=WRITE, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=dsp-streams-bian-mapper-cor-account-cor-account-state-store-repartition, patternType=LITERAL)`: 
         	(principal=User:xqdspkfkusr043, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr043, host=*, operation=DELETE, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr043, host=*, operation=READ, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=INTEGRATION.CustomerPartyKeys.CIF, patternType=LITERAL)`: 
         	(principal=User:xqdspkfkusr009, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:CMT-prod-kfkusr001, host=*, operation=READ, permissionType=ALLOW)
        	(principal=User:xqdspkfkusr010, host=*, operation=WRITE, permissionType=ALLOW)
        	(principal=User:xqCMTkfkusr1, host=*, operation=READ, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=sfp-key-translation-service-dsp-KSTREAM-REDUCE-STATE-STORE-0000000004-changelog, patternType=LITERAL)`: 
         	(principal=User:xqsfpkfkusr001, host=*, operation=READ, permissionType=ALLOW)
        	(principal=User:xqsfpkfkusr001, host=*, operation=WRITE, permissionType=ALLOW) 

        Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=BIAN.RewardPointsAccount.Notification, patternType=LITERAL)`: 
         	(principal=User:xqrewkfkusr001, host=*, operation=WRITE, permissionType=ALLOW) 

                """
        parse_results = ExternalACL.parse_acl_output(pnc_output)
        self.assertEqual(len(parse_results), 230)

        nb_acls = 0
        for res in parse_results:
            nb_acls += len(res[ExternalACL.C_ACLS])

        acls = load_from_kafka_acl_output(pnc_output)
        self.assertEqual(len(acls), nb_acls)

    def test_script_call(self):
        list_output = ExternalACL.list_acls("kafka1:9091", "/etc/kafka/secrets/client_sasl_plain.config")
        ret = ExternalACL.parse_acl_output(list_output)
        print(ret)
        self.assertEqual(len(ret), 2)

        acls = load_from_kafka_acl_output(list_output)
        print(acls)
        self.assertEqual(len(acls), 3)
