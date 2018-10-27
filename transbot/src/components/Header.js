import React from 'react'
import { Navbar, NavbarBrand } from 'reactstrap'
import profile_template from '../img/profile_template.svg'

const Header = () => (
    <Navbar color="light" light>
        <img src={profile_template} alt="..." className="rounded-circle"></img>
        <NavbarBrand>Transbot</NavbarBrand>
    </Navbar>
)

export default Header