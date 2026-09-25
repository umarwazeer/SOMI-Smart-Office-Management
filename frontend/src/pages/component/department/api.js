import api from 'src/services/api'

class DepartmentApi {
  getDepartment () {
    return api.get('/departments/')
  }

  createDepartment (department) {
    return api.post('/departments/', department)
  }

  updateDepartment (id, department) {
    return api.patch(`/departments/${id}/`, department)
  }

  deleteDepartment (id) {
    return api.delete(`/departments/${id}/`)
  }
}

export default new DepartmentApi()
