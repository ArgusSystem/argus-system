package com.example.argus.data

import org.junit.Assert.assertEquals
import org.junit.Assert.assertNotNull
import org.junit.Assert.assertNull

import org.junit.Test

class AuthenticationClientTest {
    @Test
    fun successfulLogIn() {
        val client = AuthenticationClient()
        val alias = client.logIn("argus", "panoptes")

        assertNotNull(alias)
        assertEquals("gabriel", alias)
    }

    @Test
    fun failedToLogIn() {
        val client = AuthenticationClient()
        val alias = client.logIn("fake", "client")

        assertNull(alias)
    }
}
