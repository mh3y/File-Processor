from discord_webhook import DiscordWebhook

content = "Hi I'm a little minion built by Michael"

webhook = DiscordWebhook(url="https://discord.com/api/webhooks/1012265615827939358"
                             "/iG3YuFXkEaJwrvUXsYSxDlMDTNORDqe6U9Dfa2hZh_qOL_wMfV-qI1-3-n9xRp1bR_rx", content=content)

response = webhook.execute()

