import React, {useState, useContext} from 'react'
import SocketContext from '../../context/SocketContext'
import Button2 from '../buttonsAndInputs/Button2'
import ServerControls from './ServerControls'
import { ReactComponent as ArrowUp } from '../../assets/up-chevron.svg'
import { ReactComponent as ArrowDown} from '../../assets/down-chevron.svg'
import '../../css/general.css'
import '../../css/cards-and-containers.css'

const ServerCardDropdown = ({device}) => {
    const {handleSetCurrentDevice} = useContext(SocketContext)
    const [dropDown, setDropDown] = useState(false)
  
  
    
    const toggle = async () => {
      await handleSetCurrentDevice(device.unit_id, false, null)
      setDropDown(!dropDown)
    }
  
  
    return (
      <div className='main-card-dropdown'>
        <div className='padding-10 justify-content-between w-100'>
          <div className={device.id ? 'justify-content-end display-inline w-75' : 'w-100'}>
            <h3 className='text-white'>{device.name}</h3>
          </div>
          {device.id &&
            <Button2 
            action={toggle} 
            text={dropDown ? <ArrowUp className='svg1'/> : <ArrowDown className='svg1'/> } 
            wrapperClass = 'justify-content-center'
            />
          }
          </div>
          {device.id && dropDown && (
              <ServerControls device={device} />
          )}

      </div>
    )
}

export default ServerCardDropdown