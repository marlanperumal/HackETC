import React, { Component } from 'react'
import './App.css'

import Header from './components/Header'
import ChatArea from './components/ChatArea'
import Footer from './components/Footer'

import { library } from '@fortawesome/fontawesome-svg-core'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faArrowAltCircleRight } from '@fortawesome/free-solid-svg-icons'

library.add(faArrowAltCircleRight)

class App extends Component {
    constructor(props) {
        super(props)
        this.state = {
            messages: []
        }
    }

    getReply = () => {

        this.setState({
            messages: [
                ...this.state.messages,
                {
                    side: "left",
                    text: "👍"
                }
            ]
        })
    }

    addMessage = (side, text) => {
        this.setState({
            messages: [
                ...this.state.messages,
                {
                    side,
                    text
                }
            ]
        })
        setTimeout(this.getReply, 500)
    }

    render() {
        return (
            <div className="App">
                <Header/>
                <ChatArea messages={this.state.messages} />
                <Footer onSubmit={this.addMessage}/>
            </div>
        );
    }
}

export default App
