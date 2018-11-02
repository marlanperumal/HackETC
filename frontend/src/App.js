import React, { Component } from 'react'
import './App.css'

import Header from './components/Header'
import ChatArea from './components/ChatArea'
import Footer from './components/Footer'

import { library } from '@fortawesome/fontawesome-svg-core'
import { faArrowAltCircleRight } from '@fortawesome/free-solid-svg-icons'
import { faCreativeCommonsBy } from '@fortawesome/free-brands-svg-icons'

library.add(faArrowAltCircleRight)
library.add(faCreativeCommonsBy)

const backend_host = process.env.REACT_APP_BACKEND_HOST || 'http://localhost:5000'

class App extends Component {
    constructor(props) {
        super(props)
        this.state = {
            messages: [
                {
                    side: "left",
                    text: "Hi James - I'm UDrive! Where would you like to go today?"
                },
            ],
            origin: "",
            destination: "",
            priority: "cost",
            leave_time: "now",
            arrive_time: null,
            legs: [],
            current_leg: 0,
            typing: false
        }
    }

    getReply = (message) => {
        const { origin, destination, priority, leave_time, arrive_time, legs, current_leg } = this.state
        const data = {
            message, origin, destination, priority, leave_time, arrive_time, legs, current_leg
        }
        return fetch(`${backend_host}/message`, {
            method: "POST",
            mode: "cors",
            cache: "no-cache",
            credentials: "same-origin",
            headers: {
                "Content-Type": "application/json; charset=utf-8",
            },
            redirect: "follow",
            referrer: "no-referrer",
            body: JSON.stringify(data),
        })
        .then(response => response.json())
    }

    sendMessage = (text) => {
        this.addMessage("right", text)
        this.setState({"typing": true})
        this.getReply(text)
        .then(response => {
            console.log(response)
            this.setState({
                ...response,
                messages: [
                    ...this.state.messages,
                    ...response.reply.map(msg => ({
                        side: "left",
                        text: msg
                    }))
                ],
                typing: false
            })    
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
    }

    render() {
        return (
            <div className="app">
                <Header/>
                <ChatArea messages={this.state.messages} typing={this.state.typing} />
                <Footer onSubmit={this.sendMessage}/>
            </div>
        );
    }
}

export default App
