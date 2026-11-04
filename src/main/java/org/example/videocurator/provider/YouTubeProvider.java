package org.example.videocurator.provider;

import static org.example.videocurator.domain.Models.*;

import java.util.List;
import org.example.videocurator.quota.QuotaService.Reservation;

public interface YouTubeProvider {
  Video video(String id, Reservation budget);

  List<Video> searchVideos(String topic, Reservation budget);

  Channel channel(String selector, Reservation budget);

  List<Channel> searchChannels(String topic, Reservation budget);

  PersonalData personal(Reservation budget);

  String insertPlaylist(String title, String privacy, Reservation budget);

  String insertItem(String playlistId, String videoId, int position, Reservation budget);

  List<String> playlistVideoIds(String playlistId, Reservation budget);

  String account();

  boolean fixture();
}
