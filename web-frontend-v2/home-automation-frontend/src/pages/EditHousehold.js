import React from 'react'
import AllowedPersonsCard from '../components/edithousehold/AllowedPersonsCard'
import SideBar from '../components/navbars/SideBar'

const EditHousehold = () => {
  return (
    <div className='w-100'>
        <SideBar/>
        <div className='container'>
            <AllowedPersonsCard/>
        </div>

    </div>
  )
}

export default EditHousehold