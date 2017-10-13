require 'bundler'
Bundler.require

require 'excon'
require 'json'

TOKEN = "463417531:AAGtmovT08ni1WaNRAvFo_rveVmx4jpTHR4"

GET_UPDATES_URL = "https://api.telegram.org/bot#{TOKEN}/getUpdates"
SEND_MESSAGE_URL = "https://api.telegram.org/bot#{TOKEN}/sendMessage"


def get_updates(offset: 0)
  response = Excon.new(GET_UPDATES_URL).get(query: { timeout: 0, offset: offset })
  JSON.parse(response.body)
end

def send_message(chat_id:, text:)
  response = Excon.post(SEND_MESSAGE_URL,
    body: { chat_id: chat_id, text: text }.to_json,
    headers: { "Content-Type" => "application/json" }
  )

  response_body = JSON.parse(response.body)
  raise response_body unless response_body["ok"]
end

def get_co2
  800
end

def get_temp
  42
end

@offset = 0
loop do
  updates = get_updates(offset: @offset)
  @offset = 0

  if updates["ok"]
    updates["result"].each do |result|
      if message = result["message"]
        @offset = [@offset, result["update_id"] + 1].max

        case message["text"]
        when "co2", "со2", "цо2"
          send_message(chat_id: message["chat"]["id"], text: get_co2)
        end
      end
    end
  else
    raise r
  end
end
