import React from 'react'
import { Link } from 'react-router-dom'
import Button3 from '../buttonsAndInputs/Button3'
import Button4 from '../buttonsAndInputs/Button4'

const CamControls = ({device}) => {

  return (
    <div className='w-100 justify-content-space-around padding-10'>
        <Link to={`/edit/${device.id}`}>
          <Button3
          text='Edit'
          action={null}
          />
        </Link>
        <Link to={`/camera/${device.unit_id}`}>
          <Button4
          text='Stream'
          action={null}
          />
        </Link>
  </div>
  )
}

export default CamControls