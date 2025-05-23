// src/fontawesome.js
import { library } from '@fortawesome/fontawesome-svg-core'
import {
  faUser,
  faLock,
  faEye,
  faEyeSlash,
  faArrowLeft,
  faCar,
  faHome,
  faPlus,
  faSearch,
  faUserCircle,
  faBell,
  faSignOutAlt,
  faPlusCircle,
  faCamera,
  faTrash,
  faCheck,
  faXmark,
  faArrowRight,
  faBars,
  faMinus,
  faArrowRightLong,
  faChair,
  faPhone,
  faLayerGroup,
  faUserGroup,
  faCirclePlus,
  faUserPen,
  faPencil,
  faClock

} from '@fortawesome/free-solid-svg-icons'

export function registerIcons() {
  library.add(
    faUser,
    faLock,
    faEye,
    faEyeSlash,
    faArrowLeft,
    faCar,
    faHome,
    faPlus,
    faSearch,
    faUserCircle,
    faBell,
    faSignOutAlt,
    faPlusCircle,
    faCamera,
    faTrash,
    faCheck,
    faXmark,
    faArrowRight,
    faBars,
    faMinus,
    faArrowRightLong,
    faChair,
    faPhone,
    faLayerGroup,
    faUserGroup,
    faCirclePlus,
    faUserPen,
    faPencil,
    faClock
    // 你可以继续添加更多你未来可能会用到的 icon
  )
}
