
class Services {
  constructor () {
    this.registry = {}
  }
  registerServices (servicesToRegister) {
    for (var serviceName in servicesToRegister) {
      const service = servicesToRegister[serviceName]
      this.registry[serviceName] = service
    }
  }
  use (serviceName) {
    return this.registry[serviceName]
  }
}

export default new Services()
