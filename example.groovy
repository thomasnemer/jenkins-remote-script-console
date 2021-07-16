import groovy.json.JsonOutput
def version= [:]
print JsonOutput.toJson([jenkins_version:Jenkins.instance.version.toString()])
