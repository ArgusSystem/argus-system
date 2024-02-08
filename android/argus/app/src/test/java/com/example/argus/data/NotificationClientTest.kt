package com.example.argus.data

import org.junit.Assert.assertEquals
import org.junit.Assert.assertTrue
import org.junit.Test
import java.util.concurrent.CountDownLatch
import java.util.concurrent.TimeUnit

class NotificationClientTest {

    @Test
    fun fetchNotifications() {
        val notificationClient = NotificationClient("localhost", 5000)

        val latch = CountDownLatch(1)

        notificationClient.fetch("argus", 1) { notifications ->
            assertEquals(1, notifications.size)
            latch.countDown()
        }

        assertTrue(latch.await(5, TimeUnit.SECONDS))
    }
}