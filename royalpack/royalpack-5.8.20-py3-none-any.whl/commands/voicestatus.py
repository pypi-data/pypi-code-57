from typing import *
import royalnet.serf.discord as rsd
import royalnet.commands as rc


class VoicestatusCommand(rc.Command):
    name: str = "voicestatus"

    description: str = "Visualizza lo stato interno dei voice player del bot."

    syntax: str = ""

    async def run(self, args: rc.CommandArgs, data: rc.CommandData) -> None:
        if self.interface.name != "discord":
            raise rc.UnsupportedError("Questo comando funziona solo su Discord.")
        serf: rsd.DiscordSerf = self.interface.serf

        message = []
        for index, voice_player in enumerate(serf.voice_players):
            message.append(f"🎵 [b]Voice Player #{index}[/b]")

            voice_client = voice_player.voice_client
            if voice_client.is_connected():
                message.append(f"🔵 Connected")
            else:
                message.append(f"🔴 Disconnected")
            if voice_client.is_playing():
                message.append(f"🔵 Playing")
            else:
                message.append(f"⚪ Not playing")
            if voice_client.is_paused():
                message.append(f"⚪ Paused")
            else:
                message.append(f"🔵 Not paused")

            playable = voice_player.playing
            message.append(f"🔉 {playable.__class__.__name__}")

            message.append("")

        if len(serf.voice_players) == 0:
            message.append("[i]Nessun voice player.[/i]")

        await data.reply("\n".join(message))
