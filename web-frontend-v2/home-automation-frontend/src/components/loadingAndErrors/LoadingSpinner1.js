import React from 'react'
import '../../css/loading.css'

const LoadingSpinner1 = ({size=null}) => {
  return (
    <div className={size ? `${size} lds-hourglass` : 'lds-hourglass lds-default-size'}></div>
  )
}

export default React.memo(LoadingSpinner1)