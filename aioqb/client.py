"""
Copyright (c) 2008-2021 synodriver <synodriver@gmail.com>
"""
from functools import partial
from typing import BinaryIO, List, Optional, Union
from urllib.parse import urljoin

import aiohttp
from typing_extensions import Literal

from aioqb.exceptions import (
    ApiFailedException,
    BaseQbittorrentException,
    HashNotFoundException,
    IPBanedException,
)
from aioqb.typing import JsonDumps, JsonLoads
from aioqb.utils import (
    DEFAULT_HOST,
    DEFAULT_JSON_DECODER,
    DEFAULT_JSON_ENCODER,
    DEFAULT_TIMEOUT,
)


class _BaseQbittorrentClient:
    def __init__(
        self,
        url: Optional[str] = DEFAULT_HOST,
        username: Optional[str] = None,
        password: Optional[str] = None,
        loads: JsonLoads = None,
        dumps: JsonDumps = None,
        prefix: str = "/api/v2",
    ):
        self.url = url
        self.username = username
        self.password = password
        self.loads = loads
        self.dumps = dumps
        self.prefix = prefix

    # Login
    async def auth_login(self):
        """
        Login
        :return:
        """
        data = {"username": self.username, "password": self.password}
        return await self.send_request(f"{self.prefix}/auth/login", data)

    async def auth_logout(self):
        """
        Logout
        :return:
        """
        data = None
        return await self.send_request(f"{self.prefix}/auth/logout", data)

    # Application
    # Get application version
    async def app_version(self):
        """
        Get application version
        :return:
        """
        data = None
        return await self.send_request(f"{self.prefix}/app/version", data)

    # Get API version
    async def app_webapiVersion(self):
        """
        Get API version
        :return:
        """
        data = None
        return await self.send_request(f"{self.prefix}/app/webapiVersion", data)

    # Get build info
    async def app_buildInfo(self):
        """
        Get build info
        :return:
        """
        data = None
        return await self.send_request(f"{self.prefix}/app/buildInfo", data)

    # Shutdown application
    async def app_shutdown(self):
        """
        Shutdown application
        :return:
        """
        data = None
        return await self.send_request(f"{self.prefix}/app/shutdown", data)

    # Get application preferences
    async def app_preferences(self):
        """
        Get application preferences
        :return:
        """
        data = None
        return await self.send_request(f"{self.prefix}/app/preferences", data)

    # Set application preferences
    async def app_setPreferences(
        self,
        locale: Optional[str] = None,
        create_subfolder_enabled: Optional[bool] = None,
        start_paused_enabled: Optional[bool] = None,
        auto_delete_mode: Optional[int] = None,
        preallocate_all: Optional[bool] = None,
        incomplete_files_ext: Optional[bool] = None,
        auto_tmm_enabled: Optional[bool] = None,
        torrent_changed_tmm_enabled: Optional[bool] = None,
        save_path_changed_tmm_enabled: Optional[bool] = None,
        category_changed_tmm_enabled: Optional[bool] = None,
        save_path: Optional[str] = None,
        temp_path_enabled: Optional[bool] = None,
        temp_path: Optional[str] = None,
        scan_dirs: Optional[dict] = None,
        export_dir: Optional[str] = None,
        export_dir_fin: Optional[str] = None,
        mail_notification_enabled: Optional[bool] = None,
        mail_notification_sender: Optional[str] = None,
        mail_notification_email: Optional[str] = None,
        mail_notification_smtp: Optional[str] = None,
        mail_notification_ssl_enabled: Optional[bool] = None,
        mail_notification_auth_enabled: Optional[bool] = None,
        mail_notification_username: Optional[str] = None,
        mail_notification_password: Optional[str] = None,
        autorun_enabled: Optional[bool] = None,
        autorun_program: Optional[str] = None,
        queueing_enabled: Optional[bool] = None,
        max_active_downloads: Optional[int] = None,
        max_active_torrents: Optional[int] = None,
        max_active_uploads: Optional[int] = None,
        dont_count_slow_torrents: Optional[bool] = None,
        slow_torrent_dl_rate_threshold: Optional[int] = None,
        slow_torrent_ul_rate_threshold: Optional[int] = None,
        slow_torrent_inactive_timer: Optional[int] = None,
        max_ratio_enabled: Optional[bool] = None,
        max_ratio: Optional[float] = None,
        max_ratio_act: Optional[int] = None,
        listen_port: Optional[int] = None,
        upnp: Optional[bool] = None,
        random_port: Optional[bool] = None,
        dl_limit: Optional[int] = None,
        up_limit: Optional[int] = None,
        max_connec: Optional[int] = None,
        max_connec_per_torrent: Optional[int] = None,
        max_uploads: Optional[int] = None,
        max_uploads_per_torrent: Optional[int] = None,
        stop_tracker_timeout: Optional[int] = None,
        enable_piece_extent_affinity: Optional[bool] = None,
        bittorrent_protocol: Optional[int] = None,
        limit_utp_rate: Optional[bool] = None,
        limit_tcp_overhead: Optional[bool] = None,
        limit_lan_peers: Optional[bool] = None,
        alt_dl_limit: Optional[int] = None,
        alt_up_limit: Optional[int] = None,
        scheduler_enabled: Optional[bool] = None,
        schedule_from_hour: Optional[int] = None,
        schedule_from_min: Optional[int] = None,
        schedule_to_hour: Optional[int] = None,
        schedule_to_min: Optional[int] = None,
        scheduler_days: Optional[int] = None,
        dht: Optional[bool] = None,
        pex: Optional[bool] = None,
        lsd: Optional[bool] = None,
        encryption: Optional[int] = None,
        anonymous_mode: Optional[bool] = None,
        proxy_type: Optional[int] = None,
        proxy_ip: Optional[str] = None,
        proxy_port: Optional[int] = None,
        proxy_peer_connections: Optional[bool] = None,
        proxy_auth_enabled: Optional[bool] = None,
        proxy_username: Optional[str] = None,
        proxy_password: Optional[str] = None,
        proxy_torrents_only: Optional[bool] = None,
        ip_filter_enabled: Optional[bool] = None,
        ip_filter_path: Optional[str] = None,
        ip_filter_trackers: Optional[bool] = None,
        web_ui_domain_list: Optional[str] = None,
        web_ui_address: Optional[str] = None,
        web_ui_port: Optional[int] = None,
        web_ui_upnp: Optional[bool] = None,
        web_ui_username: Optional[str] = None,
        web_ui_password: Optional[str] = None,
        web_ui_csrf_protection_enabled: Optional[bool] = None,
        web_ui_clickjacking_protection_enabled: Optional[bool] = None,
        web_ui_secure_cookie_enabled: Optional[bool] = None,
        web_ui_max_auth_fail_count: Optional[int] = None,
        web_ui_ban_duration: Optional[int] = None,
        web_ui_session_timeout: Optional[int] = None,
        web_ui_host_header_validation_enabled: Optional[bool] = None,
        bypass_local_auth: Optional[bool] = None,
        bypass_auth_subnet_whitelist_enabled: Optional[bool] = None,
        bypass_auth_subnet_whitelist: Optional[str] = None,
        alternative_webui_enabled: Optional[bool] = None,
        alternative_webui_path: Optional[str] = None,
        use_https: Optional[bool] = None,
        ssl_key: Optional[str] = None,
        ssl_cert: Optional[str] = None,
        web_ui_https_key_path: Optional[str] = None,
        web_ui_https_cert_path: Optional[str] = None,
        dyndns_enabled: Optional[bool] = None,
        dyndns_service: Optional[int] = None,
        dyndns_username: Optional[str] = None,
        dyndns_password: Optional[str] = None,
        dyndns_domain: Optional[str] = None,
        rss_refresh_interval: Optional[int] = None,
        rss_max_articles_per_feed: Optional[int] = None,
        rss_processing_enabled: Optional[bool] = None,
        rss_auto_downloading_enabled: Optional[bool] = None,
        rss_download_repack_proper_episodes: Optional[bool] = None,
        rss_smart_episode_filters: Optional[str] = None,
        add_trackers_enabled: Optional[bool] = None,
        add_trackers: Optional[str] = None,
        web_ui_use_custom_http_headers_enabled: Optional[bool] = None,
        web_ui_custom_http_headers: Optional[str] = None,
        max_seeding_time_enabled: Optional[bool] = None,
        max_seeding_time: Optional[int] = None,
        announce_ip: Optional[str] = None,
        announce_to_all_tiers: Optional[bool] = None,
        announce_to_all_trackers: Optional[bool] = None,
        async_io_threads: Optional[int] = None,
        banned_IPs: Optional[str] = None,
        checking_memory_use: Optional[int] = None,
        current_interface_address: Optional[str] = None,
        current_network_interface: Optional[str] = None,
        disk_cache: Optional[int] = None,
        disk_cache_ttl: Optional[int] = None,
        embedded_tracker_port: Optional[int] = None,
        enable_coalesce_read_write: Optional[bool] = None,
        enable_embedded_tracker: Optional[bool] = None,
        enable_multi_connections_from_same_ip: Optional[bool] = None,
        enable_os_cache: Optional[bool] = None,
        enable_upload_suggestions: Optional[bool] = None,
        file_pool_size: Optional[int] = None,
        outgoing_ports_max: Optional[int] = None,
        outgoing_ports_min: Optional[int] = None,
        recheck_completed_torrents: Optional[bool] = None,
        resolve_peer_countries: Optional[bool] = None,
        save_resume_data_interval: Optional[int] = None,
        send_buffer_low_watermark: Optional[int] = None,
        send_buffer_watermark: Optional[int] = None,
        send_buffer_watermark_factor: Optional[int] = None,
        socket_backlog_size: Optional[int] = None,
        upload_choking_algorithm: Optional[int] = None,
        upload_slots_behavior: Optional[int] = None,
        upnp_lease_duration: Optional[int] = None,
        utp_tcp_mixed_mode: Optional[int] = None,
    ):
        """
        Set application preferences
        :param locale:
        :param create_subfolder_enabled:
        :param start_paused_enabled:
        :param auto_delete_mode:
        :param preallocate_all:
        :param incomplete_files_ext:
        :param auto_tmm_enabled:
        :param torrent_changed_tmm_enabled:
        :param save_path_changed_tmm_enabled:
        :param category_changed_tmm_enabled:
        :param save_path:
        :param temp_path_enabled:
        :param temp_path:
        :param scan_dirs:
        :param export_dir:
        :param export_dir_fin:
        :param mail_notification_enabled:
        :param mail_notification_sender:
        :param mail_notification_email:
        :param mail_notification_smtp:
        :param mail_notification_ssl_enabled:
        :param mail_notification_auth_enabled:
        :param mail_notification_username:
        :param mail_notification_password:
        :param autorun_enabled:
        :param autorun_program:
        :param queueing_enabled:
        :param max_active_downloads:
        :param max_active_torrents:
        :param max_active_uploads:
        :param dont_count_slow_torrents:
        :param slow_torrent_dl_rate_threshold:
        :param slow_torrent_ul_rate_threshold:
        :param slow_torrent_inactive_timer:
        :param max_ratio_enabled:
        :param max_ratio:
        :param max_ratio_act:
        :param listen_port:
        :param upnp:
        :param random_port:
        :param dl_limit:
        :param up_limit:
        :param max_connec:
        :param max_connec_per_torrent:
        :param max_uploads:
        :param max_uploads_per_torrent:
        :param stop_tracker_timeout:
        :param enable_piece_extent_affinity:
        :param bittorrent_protocol:
        :param limit_utp_rate:
        :param limit_tcp_overhead:
        :param limit_lan_peers:
        :param alt_dl_limit:
        :param alt_up_limit:
        :param scheduler_enabled:
        :param schedule_from_hour:
        :param schedule_from_min:
        :param schedule_to_hour:
        :param schedule_to_min:
        :param scheduler_days:
        :param dht:
        :param pex:
        :param lsd:
        :param encryption:
        :param anonymous_mode:
        :param proxy_type:
        :param proxy_ip:
        :param proxy_port:
        :param proxy_peer_connections:
        :param proxy_auth_enabled:
        :param proxy_username:
        :param proxy_password:
        :param proxy_torrents_only:
        :param ip_filter_enabled:
        :param ip_filter_path:
        :param ip_filter_trackers:
        :param web_ui_domain_list:
        :param web_ui_address:
        :param web_ui_port:
        :param web_ui_upnp:
        :param web_ui_username:
        :param web_ui_password:
        :param web_ui_csrf_protection_enabled:
        :param web_ui_clickjacking_protection_enabled:
        :param web_ui_secure_cookie_enabled:
        :param web_ui_max_auth_fail_count:
        :param web_ui_ban_duration:
        :param web_ui_session_timeout:
        :param web_ui_host_header_validation_enabled:
        :param bypass_local_auth:
        :param bypass_auth_subnet_whitelist_enabled:
        :param bypass_auth_subnet_whitelist:
        :param alternative_webui_enabled:
        :param alternative_webui_path:
        :param use_https:
        :param ssl_key:
        :param ssl_cert:
        :param web_ui_https_key_path:
        :param web_ui_https_cert_path:
        :param dyndns_enabled:
        :param dyndns_service:
        :param dyndns_username:
        :param dyndns_password:
        :param dyndns_domain:
        :param rss_refresh_interval:
        :param rss_max_articles_per_feed:
        :param rss_processing_enabled:
        :param rss_auto_downloading_enabled:
        :param rss_download_repack_proper_episodes:
        :param rss_smart_episode_filters:
        :param add_trackers_enabled:
        :param add_trackers:
        :param web_ui_use_custom_http_headers_enabled:
        :param web_ui_custom_http_headers:
        :param max_seeding_time_enabled:
        :param max_seeding_time:
        :param announce_ip:
        :param announce_to_all_tiers:
        :param announce_to_all_trackers:
        :param async_io_threads:
        :param banned_IPs:
        :param checking_memory_use:
        :param current_interface_address:
        :param current_network_interface:
        :param disk_cache:
        :param disk_cache_ttl:
        :param embedded_tracker_port:
        :param enable_coalesce_read_write:
        :param enable_embedded_tracker:
        :param enable_multi_connections_from_same_ip:
        :param enable_os_cache:
        :param enable_upload_suggestions:
        :param file_pool_size:
        :param outgoing_ports_max:
        :param outgoing_ports_min:
        :param recheck_completed_torrents:
        :param resolve_peer_countries:
        :param save_resume_data_interval:
        :param send_buffer_low_watermark:
        :param send_buffer_watermark:
        :param send_buffer_watermark_factor:
        :param socket_backlog_size:
        :param upload_choking_algorithm:
        :param upload_slots_behavior:
        :param upnp_lease_duration:
        :param utp_tcp_mixed_mode:
        :return:
        """
        data = {
            "locale": locale,
            "create_subfolder_enabled": create_subfolder_enabled,
            "start_paused_enabled": start_paused_enabled,
            "auto_delete_mode": auto_delete_mode,
            "preallocate_all": preallocate_all,
            "incomplete_files_ext": incomplete_files_ext,
            "auto_tmm_enabled": auto_tmm_enabled,
            "torrent_changed_tmm_enabled": torrent_changed_tmm_enabled,
            "save_path_changed_tmm_enabled": save_path_changed_tmm_enabled,
            "category_changed_tmm_enabled": category_changed_tmm_enabled,
            "save_path": save_path,
            "temp_path_enabled": temp_path_enabled,
            "temp_path": temp_path,
            "scan_dirs": scan_dirs,
            "export_dir": export_dir,
            "export_dir_fin": export_dir_fin,
            "mail_notification_enabled": mail_notification_enabled,
            "mail_notification_sender": mail_notification_sender,
            "mail_notification_email": mail_notification_email,
            "mail_notification_smtp": mail_notification_smtp,
            "mail_notification_ssl_enabled": mail_notification_ssl_enabled,
            "mail_notification_auth_enabled": mail_notification_auth_enabled,
            "mail_notification_username": mail_notification_username,
            "mail_notification_password": mail_notification_password,
            "autorun_enabled": autorun_enabled,
            "autorun_program": autorun_program,
            "queueing_enabled": queueing_enabled,
            "max_active_downloads": max_active_downloads,
            "max_active_torrents": max_active_torrents,
            "max_active_uploads": max_active_uploads,
            "dont_count_slow_torrents": dont_count_slow_torrents,
            "slow_torrent_dl_rate_threshold": slow_torrent_dl_rate_threshold,
            "slow_torrent_ul_rate_threshold": slow_torrent_ul_rate_threshold,
            "slow_torrent_inactive_timer": slow_torrent_inactive_timer,
            "max_ratio_enabled": max_ratio_enabled,
            "max_ratio": max_ratio,
            "max_ratio_act": max_ratio_act,
            "listen_port": listen_port,
            "upnp": upnp,
            "random_port": random_port,
            "dl_limit": dl_limit,
            "up_limit": up_limit,
            "max_connec": max_connec,
            "max_connec_per_torrent": max_connec_per_torrent,
            "max_uploads": max_uploads,
            "max_uploads_per_torrent": max_uploads_per_torrent,
            "stop_tracker_timeout": stop_tracker_timeout,
            "enable_piece_extent_affinity": enable_piece_extent_affinity,
            "bittorrent_protocol": bittorrent_protocol,
            "limit_utp_rate": limit_utp_rate,
            "limit_tcp_overhead": limit_tcp_overhead,
            "limit_lan_peers": limit_lan_peers,
            "alt_dl_limit": alt_dl_limit,
            "alt_up_limit": alt_up_limit,
            "scheduler_enabled": scheduler_enabled,
            "schedule_from_hour": schedule_from_hour,
            "schedule_from_min": schedule_from_min,
            "schedule_to_hour": schedule_to_hour,
            "schedule_to_min": schedule_to_min,
            "scheduler_days": scheduler_days,
            "dht": dht,
            "pex": pex,
            "lsd": lsd,
            "encryption": encryption,
            "anonymous_mode": anonymous_mode,
            "proxy_type": proxy_type,
            "proxy_ip": proxy_ip,
            "proxy_port": proxy_port,
            "proxy_peer_connections": proxy_peer_connections,
            "proxy_auth_enabled": proxy_auth_enabled,
            "proxy_username": proxy_username,
            "proxy_password": proxy_password,
            "proxy_torrents_only": proxy_torrents_only,
            "ip_filter_enabled": ip_filter_enabled,
            "ip_filter_path": ip_filter_path,
            "ip_filter_trackers": ip_filter_trackers,
            "web_ui_domain_list": web_ui_domain_list,
            "web_ui_address": web_ui_address,
            "web_ui_port": web_ui_port,
            "web_ui_upnp": web_ui_upnp,
            "web_ui_username": web_ui_username,
            "web_ui_password": web_ui_password,
            "web_ui_csrf_protection_enabled": web_ui_csrf_protection_enabled,
            "web_ui_clickjacking_protection_enabled": web_ui_clickjacking_protection_enabled,
            "web_ui_secure_cookie_enabled": web_ui_secure_cookie_enabled,
            "web_ui_max_auth_fail_count": web_ui_max_auth_fail_count,
            "web_ui_ban_duration": web_ui_ban_duration,
            "web_ui_session_timeout": web_ui_session_timeout,
            "web_ui_host_header_validation_enabled": web_ui_host_header_validation_enabled,
            "bypass_local_auth": bypass_local_auth,
            "bypass_auth_subnet_whitelist_enabled": bypass_auth_subnet_whitelist_enabled,
            "bypass_auth_subnet_whitelist": bypass_auth_subnet_whitelist,
            "alternative_webui_enabled": alternative_webui_enabled,
            "alternative_webui_path": alternative_webui_path,
            "use_https": use_https,
            "ssl_key": ssl_key,
            "ssl_cert": ssl_cert,
            "web_ui_https_key_path": web_ui_https_key_path,
            "web_ui_https_cert_path": web_ui_https_cert_path,
            "dyndns_enabled": dyndns_enabled,
            "dyndns_service": dyndns_service,
            "dyndns_username": dyndns_username,
            "dyndns_password": dyndns_password,
            "dyndns_domain": dyndns_domain,
            "rss_refresh_interval": rss_refresh_interval,
            "rss_max_articles_per_feed": rss_max_articles_per_feed,
            "rss_processing_enabled": rss_processing_enabled,
            "rss_auto_downloading_enabled": rss_auto_downloading_enabled,
            "rss_download_repack_proper_episodes": rss_download_repack_proper_episodes,
            "rss_smart_episode_filters": rss_smart_episode_filters,
            "add_trackers_enabled": add_trackers_enabled,
            "add_trackers": add_trackers,
            "web_ui_use_custom_http_headers_enabled": web_ui_use_custom_http_headers_enabled,
            "web_ui_custom_http_headers": web_ui_custom_http_headers,
            "max_seeding_time_enabled": max_seeding_time_enabled,
            "max_seeding_time": max_seeding_time,
            "announce_ip": announce_ip,
            "announce_to_all_tiers": announce_to_all_tiers,
            "announce_to_all_trackers": announce_to_all_trackers,
            "async_io_threads": async_io_threads,
            "banned_IPs": banned_IPs,
            "checking_memory_use": checking_memory_use,
            "current_interface_address": current_interface_address,
            "current_network_interface": current_network_interface,
            "disk_cache": disk_cache,
            "disk_cache_ttl": disk_cache_ttl,
            "embedded_tracker_port": embedded_tracker_port,
            "enable_coalesce_read_write": enable_coalesce_read_write,
            "enable_embedded_tracker": enable_embedded_tracker,
            "enable_multi_connections_from_same_ip": enable_multi_connections_from_same_ip,
            "enable_os_cache": enable_os_cache,
            "enable_upload_suggestions": enable_upload_suggestions,
            "file_pool_size": file_pool_size,
            "outgoing_ports_max": outgoing_ports_max,
            "outgoing_ports_min": outgoing_ports_min,
            "recheck_completed_torrents": recheck_completed_torrents,
            "resolve_peer_countries": resolve_peer_countries,
            "save_resume_data_interval": save_resume_data_interval,
            "send_buffer_low_watermark": send_buffer_low_watermark,
            "send_buffer_watermark": send_buffer_watermark,
            "send_buffer_watermark_factor": send_buffer_watermark_factor,
            "socket_backlog_size": socket_backlog_size,
            "upload_choking_algorithm": upload_choking_algorithm,
            "upload_slots_behavior": upload_slots_behavior,
            "upnp_lease_duration": upnp_lease_duration,
            "utp_tcp_mixed_mode": utp_tcp_mixed_mode,
        }
        data = {k: v for k, v in data.items() if v is not None}
        return await self.send_request(f"{self.prefix}/app/setPreferences", data)

    # Get default save path
    async def app_defaultSavePath(self):
        """
        Get default save path
        :return:
        """
        data = None
        return await self.send_request(f"{self.prefix}/app/defaultSavePath", data)

    # Log
    # Get log
    async def log_main(
        self,
        normal: Optional[bool] = True,
        info: Optional[bool] = True,
        warning: Optional[bool] = True,
        critical: Optional[bool] = True,
        last_known_id: Optional[int] = -1,
    ):
        """
        Get log
        :param normal:          Include normal messages (default: true)
        :param info:            Include info messages (default: true)
        :param warning:         Include warning messages (default: true)
        :param critical:        Include critical messages (default: true)
        :param last_known_id:   Exclude messages with "message id" <= last_known_id (default: -1)):
        :return:
        """
        data = {
            "normal": normal,
            "info": info,
            "warning": warning,
            "critical": critical,
            "last_known_id": last_known_id,
        }
        return await self.send_request(f"{self.prefix}/log/main", data)

    # Get peer log
    async def log_peers(self, last_known_id: Optional[int] = -1):
        """
        Get peer log
        :param last_known_id: Exclude messages with "message id" <= last_known_id (default: -1)
        :return:
        """
        data = {"last_known_id": last_known_id}
        return await self.send_request(f"{self.prefix}/log/peers", data)

    # Sync
    async def sync_maindata(self, rid: Optional[int] = 0):
        """
        Get main data
        :param rid: Response ID. If not provided, rid=0 will be assumed. If the given rid is different from the one of
        last server reply, full_update will be true (see the server reply details for more info)
        :return:
        """
        data = {"rid": rid}
        return await self.send_request(f"{self.prefix}/sync/maindata", data)

    async def sync_torrentPeers(self, hash: str, rid: Optional[int] = 0):
        """
        Get torrent peers data
        :param hash:
        :param rid:
        :return:
        """
        data = {"hash": hash, "rid": rid}
        return await self.send_request(f"{self.prefix}/sync/torrentPeers", data)

    # Transfer info
    async def transfer_info(self):
        """
        Get global transfer info
        This method returns info you usually see in qBt status bar.
        :return:
        """
        data = None
        return await self.send_request(f"{self.prefix}/transfer/info", data)

    async def transfer_speedLimitsMode(self):
        """
        Get alternative speed limits state
        :return:
        """
        data = None
        return await self.send_request(f"{self.prefix}/transfer/speedLimitsMode", data)

    async def transfer_toggleSpeedLimitsMode(self):
        """
        Toggle alternative speed limits
        :return:
        """
        data = None
        return await self.send_request(
            f"{self.prefix}/transfer/toggleSpeedLimitsMode", data
        )

    async def transfer_downloadLimit(self):
        """
        Get global download limit
        :return:
        """
        data = None
        return await self.send_request(f"{self.prefix}/transfer/downloadLimit", data)

    async def transfer_setDownloadLimit(self, limit: int):
        """
        Set global download limit
        :param limit: The global download speed limit to set in bytes/second
        :return:
        """
        data = {"limit": limit}
        return await self.send_request(f"{self.prefix}/transfer/setDownloadLimit", data)

    async def transfer_uploadLimit(self):
        """
        Get global upload limit
        :return:
        """
        data = None
        return await self.send_request(f"{self.prefix}/transfer/uploadLimit", data)

    async def transfer_setUploadLimit(self, limit: int):
        """
        Set global upload limit
        :param limit: The global upload speed limit to set in bytes/second
        :return:
        """
        data = {"limit": limit}
        return await self.send_request(f"{self.prefix}/transfer/setUploadLimit", data)

    async def transfer_banPeers(self, peers: str):
        """
        Ban peers
        :param peers: The peer to ban, or multiple peers separated by a pipe |. Each peer is a colon-separated host:port
        :return:
        """
        data = {"peers": peers}
        return await self.send_request(f"{self.prefix}/transfer/banPeers", data)

    # Torrent management All Torrent management API methods are under "torrents", e.g.: /api/v2/torrents/methodName.
    async def torrents_info(
        self,
        filter: Optional[str] = None,
        category: Optional[str] = None,
        tag: Optional[str] = None,
        sort: Optional[str] = None,
        reverse: Optional[bool] = False,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        hashes: Optional[Union[str, List[str]]] = None,
    ):
        """
        Get torrent list
        :param filter: Filter torrent list by state. Allowed state filters: all, downloading, seeding, completed, paused, active, inactive, resumed, stalled, stalled_uploading, stalled_downloading, errored
        :param category: Get torrents with the given category (empty string means "without category"; no "category" parameter means "any category" <- broken until #11748 is resolved). Remember to URL-encode the category name. For example, My category becomes My%20category
        :param tag: Get torrents with the given tag (empty string means "without tag"; no "tag" parameter means "any tag". Remember to URL-encode the category name. For example, My tag becomes My%20tag
        :param sort: Sort torrents by given key. They can be sorted using any field of the response's JSON array (which are documented below) as the sort key.
        :param reverse: Enable reverse sorting. Defaults to false
        :param limit: Limit the number of torrents returned
        :param offset: Set offset (if less than 0, offset from end)
        :param hashes: Filter by hashes. Can contain multiple hashes separated by |
        :return:
        """
        hashes = hashes if isinstance(hashes, str) else "|".join(hashes)
        data = {
            "filter": filter,
            "category": category,
            "tag": tag,
            "sort": sort,
            "reverse": reverse,
            "limit": limit,
            "offset": offset,
            "hashes": hashes,
        }
        data = {k: v for k, v in data.items() if v is not None}
        return await self.send_request(f"{self.prefix}/torrents/info", data)

    async def torrents_properties(self, hash: str):
        """
        Get torrent generic properties
        Requires knowing the torrent hash. You can get it from torrents_info.
        :param hash: The hash of the torrent you want to get the generic properties of
        :return:
        """
        data = {"hash": hash}
        return await self.send_request(f"{self.prefix}/torrents/properties", data)

    async def torrents_trackers(self, hash: str):
        """
        Get torrent trackers
        Requires knowing the torrent hash. You can get it from torrents_info.
        :param hash: The hash of the torrent you want to get the trackers of
        :return:
        """
        data = {"hash": hash}
        return await self.send_request(f"{self.prefix}/torrents/trackers", data)

    async def torrents_webseeds(self, hash: str):
        """
        Get torrent web seeds
        :param hash: The hash of the torrent you want to get the webseeds of
        :return:
        """
        data = {"hash": hash}
        return await self.send_request(f"{self.prefix}/torrents/webseeds", data)

    async def torrents_files(self, hash: str, indexes: Optional[str] = None):
        """
        Get torrent contents
        Requires knowing the torrent hash. You can get it from torrents_info.
        :param hash: The hash of the torrent you want to get the contents of
        :param indexes: The indexes of the files you want to retrieve. indexes can contain multiple values separated by |.
        :return:
        """
        data = {"hash": hash, "index": indexes} if indexes else {"hash": hash}
        return await self.send_request(f"{self.prefix}/torrents/files", data)

    async def torrents_pieceStates(self, hash: str):
        """
        Get torrent pieces' states
        Requires knowing the torrent hash. You can get it from torrents_info.
        :param hash: The hash of the torrent you want to get the pieces' states of
        :return:
        """
        data = {"hash": hash}
        return await self.send_request(f"{self.prefix}/torrents/pieceStates", data)

    async def torrents_pieceHashes(self, hash: str):
        """
        Get torrent pieces' hashes
        Requires knowing the torrent hash. You can get it from torrents_info.
        :param hash: The hash of the torrent you want to get the pieces' hashes of
        :return:
        """
        data = {"hash": hash}
        return await self.send_request(f"{self.prefix}/torrents/pieceHashes", data)

    async def torrents_pause(self, hashes: str):
        """
        Pause torrents
        Requires knowing the torrent hashes. You can get it from torrents_info.
        :param hashes: The hashes of the torrents you want to pause. hashes can contain multiple hashes separated by |,
        to pause multiple torrents, or set to all, to pause all torrents.
        :return:
        """
        data = {"hashes": hashes}
        return await self.send_request(f"{self.prefix}/torrents/pause", data)

    async def torrents_resume(self, hashes: str):
        """
        Resume torrents
        Requires knowing the torrent hashes. You can get it from torrents_info.
        :param hashes: The hashes of the torrents you want to resume. hashes can contain multiple hashes separated by |,
         to resume multiple torrents, or set to all, to resume all torrents.
        :return:
        """
        data = {"hashes": hashes}
        return await self.send_request(f"{self.prefix}/torrents/resume", data)

    async def torrents_delete(self, hashes: str, deleteFiles: Optional[bool] = False):
        """
        Requires knowing the torrent hashes. You can get it from torrents_info.
        :param hashes: The hashes of the torrents you want to delete. hashes can contain multiple hashes separated by |,
         to delete multiple torrents, or set to all, to delete all torrents.
        :param deleteFiles: If set to true, the downloaded data will also be deleted, otherwise has no effect.
        :return:
        """
        data = {"hashes": hashes, "deleteFiles": deleteFiles}
        return await self.send_request(f"{self.prefix}/torrents/delete", data)

    async def torrents_recheck(self, hashes: str):
        """
        Recheck torrents
        Requires knowing the torrent hashes. You can get it from torrents_info.
        :param hashes: The hashes of the torrents you want to recheck. hashes can contain multiple hashes separated by |,
         to recheck multiple torrents, or set to all, to recheck all torrents.
        :return:
        """
        data = {"hashes": hashes}
        return await self.send_request(f"{self.prefix}/torrents/recheck", data)

    async def torrents_reannounce(self, hashes: str):
        """
        Reannounce torrents
        Requires knowing the torrent hashes. You can get it from torrents_info.
        :param hashes: The hashes of the torrents you want to reannounce. hashes can contain multiple hashes separated by
         |, to reannounce multiple torrents, or set to all, to reannounce all torrents.
        :return:
        """
        data = {"hashes": hashes}
        return await self.send_request(f"{self.prefix}/torrents/reannounce", data)

    async def torrents_add(
        self,
        urls: Optional[List[str]] = None,
        torrents: Optional[List[BinaryIO]] = None,
        savepath: Optional[str] = None,
        cookie: Optional[str] = None,
        category: Optional[str] = None,
        tags: Optional[Union[str, List[str]]] = None,
        skip_checking: Optional[Union[Literal["true", "false"], bool]] = None,
        paused: Optional[Union[Literal["true", "false"], bool]] = None,
        root_folder: Union[Literal["true", "false", "unset"], bool] = "unset",
        rename: Optional[str] = None,
        upLimit: Optional[int] = None,
        dlLimit: Optional[int] = None,
        ratioLimit: Optional[float] = None,
        seedingTimeLimit: Optional[int] = None,
        autoTMM: Optional[bool] = None,
        sequentialDownload: Optional[Union[Literal["true", "false"], bool]] = None,
        firstLastPiecePrio: Optional[Union[Literal["true", "false"], bool]] = None,
    ):
        """
        Add new torrent
        :param urls: URLs separated with newlines
        :param torrents: Raw data of torrent file. torrents can be presented multiple times.
        :param savepath: Download folder
        :param cookie: Cookie sent to download the .torrent file
        :param category: Category for the torrent
        :param tags: Tags for the torrent, split by ','
        :param skip_checking: Skip hash checking. Possible values are true, false (default)
        :param paused: Add torrents in the paused state. Possible values are true, false (default)
        :param root_folder: Create the root folder. Possible values are true, false, unset (default)
        :param rename: Rename torrent
        :param upLimit: Set torrent upload speed limit. Unit in bytes/second
        :param dlLimit: Set torrent download speed limit. Unit in bytes/second
        :param ratioLimit: Set torrent share ratio limit
        :param seedingTimeLimit: Set torrent seeding time limit. Unit in seconds
        :param autoTMM: Whether Automatic Torrent Management should be used
        :param sequentialDownload: Enable sequential download. Possible values are true, false (default)
        :param firstLastPiecePrio: Prioritize download first last piece. Possible values are true, false (default)
        :return:
        """

        data = aiohttp.FormData()
        if urls is not None:
            data.add_field("urls", "\n".join(urls))
        if torrents is not None:
            for t in torrents:
                data.add_field(
                    "torrents",
                    t,
                    content_type="application/x-bittorrent",
                    filename=t.name,
                )
        if savepath is not None:
            data.add_field("savepath", savepath)
        if cookie is not None:
            data.add_field("cookie", cookie)
        if category is not None:
            data.add_field("category", category)
        if tags is not None:
            tags = tags if isinstance(tags, str) else ",".join(tags)
            data.add_field("tags", tags)
        if skip_checking is not None:
            skip_checking = "true" if skip_checking in ("true", True) else "false"
            data.add_field("skip_checking", skip_checking)
        if paused is not None:
            paused = "true" if paused in ("true", True) else "false"
            data.add_field("paused", paused)
        if root_folder is not None:
            if root_folder in ("true", True):
                root_folder = "true"
            elif root_folder in ("false", False):
                root_folder = "false"
            else:
                root_folder = "unset"
            data.add_field("root_folder", root_folder)
        if rename is not None:
            data.add_field("rename", rename)
        if upLimit is not None:
            data.add_field("upLimit", upLimit)
        if dlLimit is not None:
            data.add_field("dlLimit", dlLimit)
        if ratioLimit is not None:
            data.add_field("ratioLimit", ratioLimit)
        if seedingTimeLimit is not None:
            data.add_field("seedingTimeLimit", seedingTimeLimit)
        if autoTMM is not None:
            data.add_field("autoTMM", autoTMM)
        if sequentialDownload is not None:
            sequentialDownload = (
                "true" if sequentialDownload in ("true", True) else "false"
            )
            data.add_field("sequentialDownload", sequentialDownload)
        if firstLastPiecePrio is not None:
            firstLastPiecePrio = (
                "true" if firstLastPiecePrio in ("true", True) else "false"
            )
            data.add_field("firstLastPiecePrio", firstLastPiecePrio)

        return await self.send_request(f"{self.prefix}/torrents/add", data)

    async def torrents_addTrackers(self, hash: str, urls: List[str]):
        """
        Add trackers to torrent
        Requires knowing the torrent hash. You can get it from torrent_info.
        :param hash:
        :param urls:
        :return:
        """
        data = {"hash": hash, "urls": "%0A".join(urls)}
        return await self.send_request(f"{self.prefix}/torrents/addTrackers", data)

    async def torrents_editTracker(self, hash: str, origUrl: str, newUrl: str):
        """
        Edit trackers
        :param hash: The hash of the torrent
        :param origUrl: The tracker URL you want to edit
        :param newUrl: The new URL to replace the origUrl
        :return:
        """
        data = {"hash": hash, "origUrl": origUrl, "newUrl": newUrl}
        return await self.send_request(f"{self.prefix}/torrents/editTracker", data)

    async def torrents_removeTrackers(self, hash: str, urls: Union[str, List[str]]):
        """
        Remove trackers
        :param hash: The hash of the torrent
        :param urls: URLs to remove, separated by |
        :return:
        """
        urls = urls if isinstance(urls, str) else "|".join(urls)
        data = {"hash": hash, "urls": urls}
        return await self.send_request(f"{self.prefix}/torrents/removeTrackers", data)

    async def torrents_addPeers(
        self, hashes: Union[str, List[str]], peers: Union[str, List[str]]
    ):
        """
        Add peers
        :param hashes: The hash of the torrent, or multiple hashes separated by a pipe |
        :param peers: The peer to add, or multiple peers separated by a pipe |. Each peer is a colon-separated host:port
        :return:
        """
        hashes = hashes if isinstance(hashes, str) else "|".join(hashes)
        peers = peers if isinstance(peers, str) else "|".join(peers)
        data = {"hashes": hashes, "peers": peers}
        return await self.send_request(f"{self.prefix}/torrents/addPeers", data)

    async def torrents_increasePrio(self, hashes: Union[str, List[str]]):
        """
        Increase torrent priority
        Requires knowing the torrent hash. You can get it from torrent_info.
        :param hashes: The hashes of the torrents you want to increase the priority of. hashes can contain multiple
        hashes separated by |, to increase the priority of multiple torrents, or set to all, to increase the priority of all torrents.
        :return:
        """
        hashes = hashes if isinstance(hashes, str) else "|".join(hashes)
        data = {"hashes": hashes}
        return await self.send_request(f"{self.prefix}/torrents/increasePrio", data)

    async def torrents_decreasePrio(self, hashes: Union[str, List[str]]):
        """
        Decrease torrent priority
        Requires knowing the torrent hash. You can get it from torrent_info.
        :param hashes: The hashes of the torrents you want to decrease the priority of. hashes can contain multiple
        hashes separated by |, to decrease the priority of multiple torrents, or set to all, to decrease the priority of all torrents.
        :return:
        """
        hashes = hashes if isinstance(hashes, str) else "|".join(hashes)
        data = {"hashes": hashes}
        return await self.send_request(f"{self.prefix}/torrents/decreasePrio", data)

    async def torrents_topPrio(self, hashes: Union[str, List[str]]):
        """
        Maximal torrent priority
        Requires knowing the torrent hash. You can get it from torrent_info.
        :param hashes: The hashes of the torrents you want to set to the maximum priority. hashes can contain multiple
         hashes separated by |, to set multiple torrents to the maximum priority, or set to all, to set all torrents to the maximum priority.
        :return:
        """
        hashes = hashes if isinstance(hashes, str) else "|".join(hashes)
        data = {"hashes": hashes}
        return await self.send_request(f"{self.prefix}/torrents/topPrio", data)

    async def torrents_bottomPrio(self, hashes: Union[str, List[str]]):
        """
        Minimal torrent priority
        Requires knowing the torrent hash. You can get it from torrent_info.
        :param hashes: The hashes of the torrents you want to set to the minimum priority. hashes can contain multiple
        hashes separated by |, to set multiple torrents to the minimum priority, or set to all, to set all torrents to the minimum priority.
        :return:
        """
        hashes = hashes
        data = {"hashes": hashes}
        return await self.send_request(f"{self.prefix}/torrents/bottomPrio", data)

    async def torrents_filePrio(
        self, hash: str, id: Union[str, List[str]], priority: int
    ):
        """
        Set file priority
        :param hash: The hash of the torrent
        :param id: File ids, separated by |
        :param priority: File priority to set (consult torrent contents API for possible values)
        :return:
        """
        id = id if isinstance(id, str) else "|".join(id)
        data = {"hash": hash, "id": id, "priority": priority}
        return await self.send_request(f"{self.prefix}/torrents/filePrio", data)

    async def torrents_downloadLimit(self, hashes: Union[str, List[str]]):
        """
        Get torrent download limit
        Requires knowing the torrent hash. You can get it from torrents_info.
        :param hashes: hashes can contain multiple hashes separated by | or set to all
        :return:
        """
        hashes = hashes if isinstance(hashes, str) else "|".join(hashes)
        data = {"hashes": hashes}
        return await self.send_request(f"{self.prefix}/torrents/downloadLimit", data)

    async def torrents_setDownloadLimit(
        self, hashes: Union[str, List[str]], limit: int
    ):
        """
        Set torrent download limit
        Requires knowing the torrent hash. You can get it from torrents_info.
        :param hashes: hashes can contain multiple hashes separated by | or set to all
        :param limit: limit is the download speed limit in bytes per second you want to set.
        :return:
        """
        hashes = hashes if isinstance(hashes, str) else "|".join(hashes)
        data = {"hashes": hashes, "limit": limit}
        return await self.send_request(f"{self.prefix}/torrents/setDownloadLimit", data)

    async def setShareLimits(
        self,
        hashes: Union[str, List[str]],
        ratioLimit: Union[int, float],
        seedingTimeLimit: int,
    ):
        """
        Set torrent share limit
        :param hashes: hashes can contain multiple hashes separated by | or set to all
        :param ratioLimit: ratioLimit is the max ratio the torrent should be seeded until.
        -2 means the global limit should be used, -1 means no limit.
        :param seedingTimeLimit: seedingTimeLimit is the max amount of time the torrent should be seeded.
        -2 means the global limit should be used, -1 means no limit.
        :return:
        """
        hashes = hashes if isinstance(hashes, str) else "|".join(hashes)
        data = {
            "hashes": hashes,
            "ratioLimit": ratioLimit,
            "seedingTimeLimit": seedingTimeLimit,
        }
        return await self.send_request(f"{self.prefix}/torrents/setShareLimits", data)

    async def torrents_uploadLimit(self, hashes: Union[str, List[str]]):
        """
        Get torrent upload limit
        Requires knowing the torrent hash. You can get it from torrents_info.
        :param hashes: hashes can contain multiple hashes separated by | or set to all
        :return:
        """
        hashes = hashes if isinstance(hashes, str) else "|".join(hashes)
        data = {"hashes": hashes}
        return await self.send_request(f"{self.prefix}/torrents/uploadLimit", data)

    async def torrents_setUploadLimit(self, hashes: Union[str, List[str]], limit: int):
        """
        Set torrent upload limit
        Requires knowing the torrent hash. You can get it from torrents_info.
        :param hashes: hashes can contain multiple hashes separated by | or set to all
        :param limit: limit is the upload speed limit in bytes per second you want to set.
        :return:
        """
        hashes = hashes if isinstance(hashes, str) else "|".join(hashes)
        data = {"hashes": hashes, "limit": limit}
        return await self.send_request(f"{self.prefix}/torrents/setUploadLimit", data)

    async def torrents_setLocation(self, hashes: Union[str, List[str]], location: str):
        """
        Set torrent location
        Requires knowing the torrent hash. You can get it from torrents_info.
        :param hashes: hashes can contain multiple hashes separated by | or set to all
        :param location: location is the location to download the torrent to. If the location doesn't exist,
         the torrent's location is unchanged.
        :return:
        """
        hashes = hashes if isinstance(hashes, str) else "|".join(hashes)
        data = {"hashes": hashes, "location": location}
        return await self.send_request(f"{self.prefix}/torrents/setLocation", data)

    async def torrents_rename(self, hash: str, name: str):
        """
        Set torrent name
        :param hash:
        :param name:
        :return:
        """
        data = {"hash": hash, "name": name}
        return await self.send_request(f"{self.prefix}/torrents/rename", data)

    async def torrents_setCategory(self, hashes: Union[str, List[str]], category: str):
        """
        Set torrent category
        Requires knowing the torrent hash. You can get it from torrents_info.
        :param hashes: hashes can contain multiple hashes separated by | or set to all
        :param category: category is the torrent category you want to set.
        :return:
        """
        hashes = hashes if isinstance(hashes, str) else "|".join(hashes)
        data = {"hashes": hashes, "category": category}
        return await self.send_request(f"{self.prefix}/torrents/setCategory", data)

    async def torrents_categories(self):
        """
        Get all categories
        :return:
        """
        data = None
        return await self.send_request(f"{self.prefix}/torrents/categories", data)

    async def torrents_createCategory(self, category: str, savePath: str):
        """
        Add new category
        :param category: category is the category you want to create.
        :param savePath:
        :return:
        """
        data = {"category": category, "savePath": savePath}
        return await self.send_request(f"{self.prefix}/torrents/createCategory", data)

    async def torrents_editCategory(self, category: str, savePath: str):
        """
        Edit category
        :param category:
        :param savePath:
        :return:
        """
        data = {"category": category, "savePath": savePath}
        return await self.send_request(f"{self.prefix}/torrents/editCategory", data)

    async def torrents_removeCategories(self, categories: Union[str, List[str]]):
        """
        Remove categories
        :param categories: categories can contain multiple cateogies separated by \n (%0A urlencoded)
        :return:
        """
        categories = (
            categories if isinstance(categories, str) else "%0A".join(categories)
        )
        data = {"categories": categories}
        return await self.send_request(f"{self.prefix}/torrents/removeCategories", data)

    async def torrents_addTags(
        self, hashes: Union[str, List[str]], tags: Union[str, List[str]]
    ):
        """
        Add torrent tags
        Requires knowing the torrent hash. You can get it from torrents_info.
        :param hashes: hashes can contain multiple hashes separated by | or set to all
        :param tags: tags is the list of tags you want to add to passed torrents.
        :return:
        """
        hashes = hashes if isinstance(hashes, str) else "|".join(hashes)
        tags = tags if isinstance(tags, str) else ",".join(tags)
        data = {"hashes": hashes, "tags": tags}
        return await self.send_request(f"{self.prefix}/torrents/addTags", data)

    async def torrents_removeTags(
        self, hashes: Union[str, List[str]], tags: Union[str, List[str]]
    ):
        """
        Remove torrent tags
        Requires knowing the torrent hash. You can get it from torrents_info.
        :param hashes: hashes can contain multiple hashes separated by | or set to all
        :param tags: tags is the list of tags you want to remove from passed torrents. Empty list removes all tags from relevant torrents.
        :return:
        """
        hashes = hashes if isinstance(hashes, str) else "|".join(hashes)
        tags = tags if isinstance(tags, str) else ",".join(tags)
        data = {"hashes": hashes, "tags": tags}
        return await self.send_request(f"{self.prefix}/torrents/removeTags", data)

    async def torrents_tags(self):
        """
        Get all tags
        :return:
        """
        data = None
        return await self.send_request(f"{self.prefix}/torrents/tags", data)

    async def torrents_createTags(self, tags: Union[str, List[str]]):
        """
        Create tags
        :param tags: tags is a list of tags you want to create. Can contain multiple tags separated by ,.
        :return:
        """
        tags = tags if isinstance(tags, str) else ",".join(tags)
        data = {"tags": tags}
        return await self.send_request(f"{self.prefix}/torrents/createTags", data)

    async def torrents_deleteTags(self, tags: Union[str, List[str]]):
        """
        Delete tags
        :param tags: tags is a list of tags you want to delete. Can contain multiple tags separated by ,.
        :return:
        """
        tags = tags if isinstance(tags, str) else ",".join(tags)
        data = {"tags": tags}
        return await self.send_request(f"{self.prefix}/torrents/deleteTags", data)

    async def torrents_setAutoManagement(
        self, hashes: Union[str, List[str]], enable: Optional[bool] = False
    ):
        """
        Set automatic torrent management
        :param hashes: hashes can contain multiple hashes separated by | or set to all
        :param enable: enable is a boolean, affects the torrents listed in hashes, default is false
        :return:
        """
        hashes = hashes if isinstance(hashes, str) else "|".join(hashes)
        data = {"hashes": hashes, "enable": enable}
        return await self.send_request(
            f"{self.prefix}/torrents/setAutoManagement", data
        )

    async def torrents_toggleSequentialDownload(self, hashes: Union[str, List[str]]):
        """
        Toggle sequential download
        Requires knowing the torrent hash. You can get it from torrents_info.
        :param hashes: The hashes of the torrents you want to toggle sequential download for. hashes can contain
        multiple hashes separated by |, to toggle sequential download for multiple torrents, or set to all, to toggle sequential download for all torrents.
        :return:
        """
        hashes = hashes if isinstance(hashes, str) else "|".join(hashes)
        data = {"hashes": hashes}
        return await self.send_request(
            f"{self.prefix}/torrents/toggleSequentialDownload", data
        )

    async def torrents_toggleFirstLastPiecePrio(self, hashes: Union[str, List[str]]):
        """
        Set first/last piece priority
        Requires knowing the torrent hash. You can get it from torrents_info.
        :param hashes: The hashes of the torrents you want to toggle the first/last piece priority for. hashes can
        contain multiple hashes separated by |, to toggle the first/last piece priority for multiple torrents,
        or set to all, to toggle the first/last piece priority for all torrents.
        :return:
        """
        hashes = hashes if isinstance(hashes, str) else "|".join(hashes)
        data = {"hashes": hashes}
        return await self.send_request(
            f"{self.prefix}/torrents/toggleFirstLastPiecePrio", data
        )

    async def torrents_setForceStart(
        self, hashes: Union[str, List[str]], value: Optional[bool] = False
    ):
        """
        Set force start
        :param hashes: hashes can contain multiple hashes separated by | or set to all
        :param value: value is a boolean, affects the torrents listed in hashes, default is false
        :return:
        """

        hashes = hashes if isinstance(hashes, str) else "|".join(hashes)
        data = {"hashes": hashes, "value": value}
        return await self.send_request(f"{self.prefix}/torrents/setForceStart", data)

    async def torrents_setSuperSeeding(
        self, hashes: Union[str, List[str]], value: Optional[bool] = False
    ):
        """
        Set super seeding
        :param hashes: hashes can contain multiple hashes separated by | or set to all
        :param value: value is a boolean, affects the torrents listed in hashes, default is false
        :return:
        """
        hashes = hashes if isinstance(hashes, str) else "|".join(hashes)
        data = {"hashes": hashes, "value": value}
        return await self.send_request(f"{self.prefix}/torrents/setSuperSeeding", data)

    async def torrents_renameFile(self, hash: str, oldPath: str, newPath: str):
        """
        Rename file
        :param hash: The hash of the torrent
        :param oldPath: The old path of the torrent
        :param newPath: The new path to use for the file
        :return:
        """
        data = {"hash": hash, "oldPath": oldPath, "newPath": newPath}
        return await self.send_request(f"{self.prefix}/torrents/renameFile", data)

    async def torrents_renameFolder(self, hash: str, oldPath: str, newPath: str):
        """
        Rename folder
        :param hash: The hash of the torrent
        :param oldPath: The old path of the torrent
        :param newPath: The new path to use for the file
        :return:
        """
        data = {"hash": hash, "oldPath": oldPath, "newPath": newPath}
        return await self.send_request(f"{self.prefix}/torrents/renameFolder", data)

    # RSS (experimental) /api/v2/rss/methodName.
    async def rss_addFolder(self, path: str):
        """
        Add folder
        :param path: Full path of added folder (e.g. "The Pirate Bay\Top100")
        :return:
        """
        data = {"path": path}
        return await self.send_request(f"{self.prefix}/rss/addFolder", data)

    async def rss_addFeed(self, url: str, path: Optional[str]):
        """
        Add feed
        :param url: URL of RSS feed (e.g. "http://thepiratebay.org/rss//top100/200")
        :param path: Full path of added folder (e.g. "The Pirate Bay\Top100\Video")
        :return:
        """
        data = {"url": url, "path": path}
        return await self.send_request(f"{self.prefix}/rss/addFeed", data)

    async def rss_removeItem(self, path: str):
        """
        Remove item
        Removes folder or feed.
        :param path: Full path of removed item (e.g. "The Pirate Bay\Top100")
        :return:
        """
        data = {"path": path}
        return await self.send_request(f"{self.prefix}/rss/removeItem", data)

    async def rss_moveItem(self, itemPath: str, destPath: str):
        """
        Moves/renames folder or feed.
        :param itemPath: Current full path of item (e.g. "The Pirate Bay\Top100")
        :param destPath: New full path of item (e.g. "The Pirate Bay")
        :return:
        """
        data = {"itemPath": itemPath, "destPath": destPath}
        return await self.send_request(f"{self.prefix}/rss/moveItem", data)

    async def rss_items(self, withData: Optional[bool] = False):
        """
        Get all items
        :param withData: True if you need current feed articles
        :return:
        """
        data = {"withData": withData}
        return await self.send_request(f"{self.prefix}/rss/items", data)

    async def rss_markAsRead(self, itemPath: str, articleId: Optional[str] = None):
        """
        If articleId is provided only the article is marked as read otherwise the whole feed is going to be marked as read.
        :param itemPath:
        :param articleId:
        :return:
        """
        data = (
            {"itemPath": itemPath}
            if articleId is None
            else {"itemPath": itemPath, "articleId": articleId}
        )
        return await self.send_request(f"{self.prefix}/rss/markAsRead", data)

    async def rss_refreshItem(self, itemPath: str):
        """
        Refreshes folder or feed.
        :param itemPath: Current full path of item (e.g. "The Pirate Bay\Top100")
        :return:
        """
        data = {"itemPath": itemPath}
        return await self.send_request(f"{self.prefix}/rss/refreshItem", data)

    async def rss_setRule(
        self,
        ruleName: str,
        enabled: Optional[bool] = None,
        mustContain: Optional[str] = None,
        mustNotContain: Optional[str] = None,
        useRegex: Optional[bool] = None,
        episodeFilter: Optional[str] = None,
        smartFilter: Optional[bool] = None,
        previouslyMatchedEpisodes: Optional[list] = None,
        affectedFeeds: Optional[list] = None,
        ignoreDays: Optional[int] = None,
        lastMatch: Optional[str] = None,
        addPaused: Optional[bool] = None,
        assignedCategory: Optional[str] = None,
        savePath: Optional[str] = None,
    ):
        """
        Set auto-downloading rule
        :param ruleName:                        Rule name (e.g. "Punisher")
        :param enabled:                          Whether the rule is enabled
        :param mustContain:                      The sub:str that the torrent name must contain
        :param mustNotContain:                      The sub:str that the torrent name must not contain
        :param useRegex:                         	Enable regex mode in "mustContain" and "mustNotContain"
        :param episodeFilter:                        	Episode filter definition
        :param smartFilter:                       	Enable smart episode filter
        :param previouslyMatchedEpisodes:        The list of episode IDs already matched by smart filter
        :param affectedFeeds:                      The feed URLs the rule applied to
        :param ignoreDays:                       Ignore sunsequent rule matches
        :param lastMatch:                        	The rule last match time
        :param addPaused:                          Add matched torrent in paused mode
        :param assignedCategory:                   Assign category to the torrent
        :param savePath:                          Save torrent to the given directory
        :return:
        """
        ruleDef = {
            "enabled": enabled,
            "mustContain": mustContain,
            "mustNotContain": mustNotContain,
            "useRegex": useRegex,
            "episodeFilter": episodeFilter,
            "smartFilter": smartFilter,
            "previouslyMatchedEpisodes": previouslyMatchedEpisodes,
            "affectedFeeds": affectedFeeds,
            "ignoreDays": ignoreDays,
            "lastMatch": lastMatch,
            "addPaused": addPaused,
            "assignedCategory": assignedCategory,
            "savePath": savePath,
        }
        ruleDef = {k: v for k, v in ruleDef.items() if v is not None}
        ruleDef: str = self.dumps(ruleDef)
        data = {"ruleName": ruleName, "ruleDef": ruleDef}
        return await self.send_request(f"{self.prefix}/rss/setRule", data)

    async def rss_renameRule(self, ruleName: str, newRuleName: str):
        """
        Rename auto-downloading rule
        :param ruleName: Rule name (e.g. "Punisher")
        :param newRuleName: New rule name (e.g. "The Punisher")
        :return:
        """
        data = {"ruleName": ruleName, "newRuleName": newRuleName}
        return await self.send_request(f"{self.prefix}/rss/renameRule", data)

    async def rss_removeRule(self, ruleName: str):
        """
        Remove auto-downloading rule
        :param ruleName: Rule name (e.g. "Punisher")
        :return:
        """
        data = {"ruleName": ruleName}
        return await self.send_request(f"{self.prefix}/rss/removeRule", data)

    async def rss_rules(self):
        """
        Get all auto-downloading rules
        :return:
        """
        data = None
        return await self.send_request(f"{self.prefix}/rss/rules", data)

    async def rss_matchingArticles(self, ruleName: str):
        """
        Get all articles matching a rule
        :param ruleName: Rule name (e.g. "Linux")
        :return:
        """
        data = {"ruleName": ruleName}
        return await self.send_request(f"{self.prefix}/rss/matchingArticles", data)

    # Search /api/v2/search/methodName.

    async def search_start(self, pattern: str, plugins: str, category: str):
        """
        Start search
        :param pattern: Pattern to search for (e.g. "Ubuntu 18.04")
        :param plugins: Plugins to use for searching (e.g. "legittorrents"). Supports multiple plugins separated by |. Also supports all and enabled
        :param category: Categories to limit your search to (e.g. "legittorrents"). Available categories depend on the specified plugins. Also supports all
        :return:
        """
        data = {"pattern": pattern, "plugins": plugins, "category": category}
        return await self.send_request(f"{self.prefix}/search/start", data)

    async def search_stop(self, id: int):
        """
        Stop search
        :param id:
        :return:
        """
        data = {"id": id}
        return await self.send_request(f"{self.prefix}/search/stop", data)

    async def search_status(self, id: Optional[int] = None):
        """
        Get search status
        :param id: ID of the search job. If not specified, all search jobs are returned
        :return:
        """
        data = {"id": id} if id is not None else None
        return await self.send_request(f"{self.prefix}/search/status", data)

    async def search_results(
        self, id: int, limit: Optional[int] = 0, offset: Optional[int] = 0
    ):
        """
        Get search results
        :param id: ID of the search job
        :param limit: max number of results to return. 0 or negative means no limit
        :param offset: result to start at. A negative number means count backwards (e.g. -2 returns the 2 most recent results)
        :return:
        """
        data = {"id": id, "limit": limit, "offset": offset}
        return await self.send_request(f"{self.prefix}/search/results", data)

    async def search_delete(self, id: int):
        """
        Delete search
        :param id: ID of the search job
        :return:
        """
        data = {"id": id}
        return await self.send_request(f"{self.prefix}/search/delete", data)

    async def search_plugins(self):
        """
        Get search plugins
        :return:
        """
        data = None
        return await self.send_request(f"{self.prefix}/search/plugins", data)

    async def search_installPlugin(self, sources: str):
        """
        Install search plugin
        :param sources: Url or file path of the plugin to install
        (e.g. "https://raw.githubusercontent.com/qbittorrent/search-plugins/master/nova3/engines/legittorrents.py"). Supports multiple sources separated by |
        :return:
        """
        data = {"sources": sources}
        return await self.send_request(f"{self.prefix}/search/installPlugin", data)

    async def search_uninstallPlugin(self, names: Union[str, List[str]]):
        """
        Uninstall search plugin
        :param names:  Name of the plugin to uninstall (e.g. "legittorrents"). Supports multiple names separated by |
        :return:
        """
        names = names if isinstance(names, str) else "|".join(names)
        data = {"names": names}
        return await self.send_request(f"{self.prefix}/search/uninstallPlugin", data)

    async def search_enablePlugin(self, names: Union[str, List[str]], enable: bool):
        """
        Enable search plugin
        :param names: Name of the plugin to enable/disable (e.g. "legittorrents"). Supports multiple names separated by |
        :param enable: Whether the plugins should be enabled
        :return:
        """
        names = names if isinstance(names, str) else "|".join(names)
        data = {"names": names, "enable": enable}
        return await self.send_request(f"{self.prefix}/search/enablePlugin", data)

    async def search_updatePlugins(self):
        """
        Update search plugins
        :return:
        """
        data = None
        return await self.send_request(f"{self.prefix}/search/updatePlugins", data)

    async def send_request(self, endpoint: str, data, method: str = "POST"):
        raise NotImplementedError


class QbittorrentClient(_BaseQbittorrentClient):
    def __init__(
        self,
        url: Optional[str] = DEFAULT_HOST,
        username: Optional[str] = None,
        password: Optional[str] = None,
        timeout: Union[int, float] = DEFAULT_TIMEOUT,
        **kwargs,
    ):
        self.timeout = timeout
        self.kwargs = kwargs  # 用于session.post
        loads = (
            self.kwargs.pop("loads") if "loads" in self.kwargs else DEFAULT_JSON_DECODER
        )  # json serialize
        dumps = (
            self.kwargs.pop("dumps") if "dumps" in self.kwargs else DEFAULT_JSON_ENCODER
        )
        super().__init__(url, username, password, loads, dumps)
        self.client_session = aiohttp.ClientSession(
            json_serialize=self.dumps, cookie_jar=aiohttp.CookieJar(unsafe=True)
        )

    def __getattr__(self, func: str):
        parts = func.split("_")
        endpoint: str = self.prefix + "/" + "/".join(parts)

        async def pfunc(method: str = "POST", **data):
            if not data:
                data = None
            return await self.send_request(endpoint, data, method)

        return pfunc

    async def send_request(self, endpoint: str, data, method: str = "POST"):
        async with self.client_session.request(
            method,
            urljoin(self.url, endpoint),
            data=data,
            timeout=self.timeout,
            **self.kwargs,
        ) as resp:
            status = resp.status
            if status != 200:
                if status == 403:
                    raise IPBanedException(await resp.text())
                elif status == 404:
                    raise HashNotFoundException(await resp.text)
                elif status == 409:
                    raise ApiFailedException(await resp.text)
                else:
                    raise BaseQbittorrentException(await resp.text)
            try:
                return await resp.json(loads=self.loads)
            except:
                return await resp.text()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client_session.close()
