import api from 'src/services/api'

class EmployeeApi {
  getEmployees () {
    return api.get('/employees/')
  }

  getEmployee (id) {
    return api.get(`/employees/${id}/`)
  }

  createEmployee (employee) {
    const config = {}

    if (employee instanceof FormData) {
      config.headers = {
        'Content-Type': 'multipart/form-data'
      }
    }

    return api.post(
      '/employees/',
      employee,
      config
    )
  }

  updateEmployee (id, employee) {
    const config = {}

    if (employee instanceof FormData) {
      config.headers = {
        'Content-Type': 'multipart/form-data'
      }
    }

    return api.patch(
      `/employees/${id}/`,
      employee,
      config
    )
  }

  deleteEmployee (id) {
    return api.delete(`/employees/${id}/`)
  }
}

export default new EmployeeApi()
