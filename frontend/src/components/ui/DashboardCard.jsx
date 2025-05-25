import React from 'react'

const DashboardCard = ({children, label, value, className}) => {
  return (
    <div className={className}>
        {children}
    <p className='text-base text-content-secondary font-semibold mb-4'>{label}</p>
    <p className='text-[22px] text-primary'>{value}</p>
    </div>
  )
}

export default DashboardCard