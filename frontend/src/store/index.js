import { store } from 'quasar/wrappers'
import vuexStore from './store'

export default store(function () {
  return vuexStore
})
