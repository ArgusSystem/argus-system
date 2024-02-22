package com.example.argus.data

import org.junit.Assert.assertEquals
import org.junit.Assert.assertNotNull
import org.junit.Assert.assertNull
import org.junit.Assert.fail

import org.junit.Test

class AuthenticationClientTest {
    @Test
    fun successfulLogIn() {
        val client = AuthenticationClient()

        client.logIn("argus", "panoptes", { alias ->
            assertNotNull(alias)
            assertEquals("gabriel", alias)
        }, {})
    }

    @Test
    fun failedToLogIn() {
        val client = AuthenticationClient()
        client.logIn("fake", "client", {
            fail()
        }, {})
    }
}
