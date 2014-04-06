service {
extend "../../../services/puppet-agent"
 name "oracle_xe"
 icon "oracle_database.png"
 type "DATABASE"
 
 lifecycle{
 
 def oraPort = 1521
 
 startDetectionTimeoutSecs 900
 
 startDetection { 
 ServiceUtils.isPortOccupied(oraPort)
 }
 
 locator { 
 //hack to avoid monitoring started processes by cloudify
 //return [] as LinkedList 
 
 def myPids = 
ServiceUtils.ProcessUtils.getPidsWithQuery("State.Name.re=xe_pmon_XE")
 println ":pmon: current PIDs: ${myPids}"
 return myPids
 }
 
 details {
 def currPublicIP
 
 if ( context.isLocalCloud() ) {
 currPublicIP = InetAddress.localHost.hostAddress 
 }
 }
}
}
