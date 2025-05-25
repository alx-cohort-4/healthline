import React from 'react'

export const DashboardHeading = ({title, description}) => {
  return (
    <div>
        <h1 className='text-2xl text-black/87'>{title}</h1>
        <p className='text-base mt-2 text-black/60'>{description}</p>
        <hr className='text-[#CCCCCC] h-[10px] mt-4'/>
    </div>
  )
}
