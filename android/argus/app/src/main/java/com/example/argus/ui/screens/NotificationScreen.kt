package com.example.argus.ui.screens

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.aspectRatio
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.ArrowBack
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.material3.TopAppBar
import androidx.compose.material3.TopAppBarDefaults
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.res.integerResource
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import coil.compose.AsyncImage
import com.example.argus.ArgusScreen
import com.example.argus.R
import com.example.argus.data.NotificationClient
import com.example.argus.model.Notification
import com.example.argus.model.NotificationFace
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale


@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun NotificationTopBar(
    navigateUp: () -> Unit,
    modifier: Modifier = Modifier
) {
    TopAppBar(
        title = {
            Text(stringResource(ArgusScreen.Notification.title))
        },
        colors = TopAppBarDefaults.mediumTopAppBarColors(
            containerColor = MaterialTheme.colorScheme.primaryContainer
        ),
        modifier = modifier,
        navigationIcon = {
            IconButton(onClick = {
                navigateUp()
            }) {
                Icon(
                    imageVector = Icons.Filled.ArrowBack,
                    contentDescription = stringResource(R.string.back_button)
                )
            }
        }
    )
}

@Composable
fun NotificationScreen(notification: Notification, notificationClient: NotificationClient, navigateUp: () -> Unit, modifier: Modifier = Modifier) {
    var notificationFaces by remember {
        mutableStateOf(emptyList<NotificationFace>())
    }

    notificationClient.fetchNotificationFaces(notification) { notificationFaces = it }

    val host = stringResource(id = R.string.api_host)
    val port = integerResource(id = R.integer.api_port)

    val details = listOf(
        Detail(name = stringResource(R.string.notification_person_detail), value = notification.person),
        Detail(name = stringResource(R.string.notification_place_detail), value = notification.place),
        Detail(name = stringResource(R.string.notification_start_time_detail), value = formatTimestamp(notification.startTime)),
        Detail(name = stringResource(R.string.notification_end_time_detail), value = formatTimestamp(notification.endTime))
    )

    Scaffold(
        topBar = {
            NotificationTopBar(navigateUp = navigateUp)
        }
    ) { innerPadding ->
        LazyColumn(
            modifier = modifier.padding(innerPadding)
        ) {
            items(details) { detail ->
                ItemRow(detail)
            }

            items(notificationFaces.chunked(3)) { row ->
                Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
                    for (notificationFace in row) {
                        FaceImage(imageUrl = "http://$host:$port/faces/${notificationFace.imageKey}")
                    }
                }
            }
        }
    }

}

@Composable
private fun ItemRow(detail: Detail) {
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .padding(8.dp),
        horizontalArrangement = Arrangement.SpaceBetween) {
        Text(text = detail.name, fontWeight = FontWeight.Bold)
        Text(text = detail.value)
    }
}

@Composable
fun FaceImage(imageUrl : String) {
    AsyncImage(
        model = imageUrl,
        contentDescription = null,
        modifier = Modifier
            .padding(4.dp)
            .size(120.dp)
            .aspectRatio(1f), // Maintain aspect ratio
        contentScale = ContentScale.Crop // Crop the image if necessary
    )
}

fun formatTimestamp(timestamp: Long): String {
    val sdf = SimpleDateFormat("yyyy-MM-dd HH:mm:ss", Locale.getDefault())
    return sdf.format(Date(timestamp))
}

private data class Detail(
    val name: String,
    val value: String
)