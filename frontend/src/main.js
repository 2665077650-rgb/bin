import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import './styles/main.css'

// 引入组件库
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'

// 引入图标库
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { library } from '@fortawesome/fontawesome-svg-core'
import {
  faHome,
  faCompass,
  faMap,
  faPuzzlePiece,
  faHistory,
  faSearch,
  faUser,
  faVolumeUp,
  faPalette,
  faCamera,
  faStar,
  faHeart,
  faShare,
  faBookmark,
  faInfoCircle,
  faArrowLeft,
  faArrowRight,
  faExpand,
  faCompress,
  faRotateLeft,
  faRobot,
  faMicrophone,
  faKeyboard,
  faLightbulb,
  faTimes
} from '@fortawesome/free-solid-svg-icons'

library.add(
  faHome, faCompass, faMap, faPuzzlePiece, faHistory,
  faSearch, faUser, faVolumeUp, faPalette, faCamera,
  faStar, faHeart, faShare, faBookmark, faInfoCircle,
  faArrowLeft, faArrowRight, faExpand, faCompress,
  faRotateLeft, faRobot, faMicrophone, faKeyboard,
  faLightbulb, faTimes
)

const app = createApp(App)

app.use(router)
app.use(ElementPlus)
app.component('FontAwesomeIcon', FontAwesomeIcon)

app.mount('#app')