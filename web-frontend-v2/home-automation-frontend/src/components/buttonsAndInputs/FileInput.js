import React from 'react'
import {ReactComponent as MediaUplaodBtn} from '../../assets/picture-frame.svg'

const FileInput = ({id=null, classWrapper='', multipleFiles=false, labelText=null, onChange=null}) => {
  return (
    <div className={classWrapper}>
        {multipleFiles ? 
            <>
                <label htmlFor={id}>
                    <input multiple  id={id} onChange={onChange} name={id} type='file' accept='image/jpeg, image/png, video/mp4' hidden/> 
                    {labelText ? labelText : <MediaUplaodBtn className='svg2'/>}
                </label>
            </>
            :   
            <>
                <label htmlFor={id}>
                    <input id={id} name={id} onChange={onChange}  type='file' accept='image/jpeg, image/png, video/mp4' hidden/>  
                    {labelText ? labelText : <MediaUplaodBtn className='svg2'/>}
                </label>
            </>
        }
    </div>
  )
}

export default FileInput