package com.example.argus.ui.screens

import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material3.Card
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp

@Composable
fun NotificationsScreen(modifier: Modifier = Modifier) {
    val notifications = getNotifications()
    LazyColumn(modifier = modifier) {
        items(notifications) { notification ->
            NotificationCard(notification = notification, modifier = Modifier.padding(8.dp))
        }
    }
}

@Composable
fun NotificationCard(notification: String, modifier: Modifier = Modifier) {
    Card(modifier = modifier) {
        Text(
            text = notification,
            modifier = Modifier.padding(16.dp),
            style = MaterialTheme.typography.headlineSmall
        )
    }
}

fun getNotifications() : List<String> {
    return listOf(
        "Just",
        "a",
        "very",
        "long",
        "test",
        "to",
        "show",
        "a",
        "long",
        "scrollable",
        "list"
    )
}

@Preview
@Composable
fun NotificationScreenPreview() {
    NotificationsScreen()
}