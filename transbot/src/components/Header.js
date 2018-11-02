import React from 'react'
import { Navbar, NavbarBrand } from 'reactstrap'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'


const Header = () => (
    <Navbar color="light" light>
        <FontAwesomeIcon icon={["fab", "creative-commons-by"]} size="4x"/>
        <NavbarBrand>UDrive</NavbarBrand>
    </Navbar>
)

export default Header