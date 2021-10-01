import groovy.json.JsonOutput
def result = [:]

result["jenkins_version"] = Jenkins.instance.version.toString()

print JsonOutput.toJson(result)
