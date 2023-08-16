import React from 'react'
import { Link, useHistory} from 'react-router-dom'
import Button3 from '../buttonsAndInputs/Button3'


const ServerControls = ({device}) => {

  const history = useHistory()

  return (
    <div  className='w-100 justify-content-space-around padding-10'>
        <Link to={`/edit/${device.id}`}>
          <Button3
          text='Edit'
          action={() => {history.push(`edit-server/${device.id}`)}}
          />
        </Link>
        
  </div>
  )
}

export default ServerControls