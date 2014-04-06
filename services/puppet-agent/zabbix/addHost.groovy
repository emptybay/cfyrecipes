import org.cloudifysource.utilitydomain.context.ServiceContextFactory
import java.io.File

// Calling addHost python script

println "######################Calling addHost python script"

def context = ServiceContextFactory.getServiceContext()
println "got context"
println "service name is " + context.serviceName

def config = new ConfigSlurper().parse(new File(context.serviceName + "-service.properties").toURL())
println "got proerties file"

def hostIP = context.privateAddress
def templateIDs = config.zabbixTemplateIds

def command = "python " + context.serviceDirectory + "/zabbix/python/addHost.py add " + hostIP + " " + templateIDs
println "running command " + command
def proc = command.execute()
proc.waitFor()

// Obtain status and output
println "return code: ${ proc.exitValue()}"
println "stderr: ${proc.err.text}"
println "stdout: ${proc.in.text}" // *out* from the external program is *in* for groovy