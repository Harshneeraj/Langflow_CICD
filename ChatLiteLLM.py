from langchain_community.chat_models.litellm import ChatLiteLLM, ChatLiteLLMException
from langflow.base.constants import STREAM_INFO_TEXT
from langflow.base.models.model import LCModelComponent
from langflow.field_typing import LanguageModel
from langflow.io import (
    BoolInput,
    DictInput,
    DropdownInput,
    FloatInput,
    IntInput,
    MessageInput,
    SecretStrInput,
    StrInput,
)



class ChatLiteLLMModelComponent(LCModelComponent):
    display_name = "LiteLLM"
    description = "`LiteLLM` collection of large language models."
    documentation = "https://python.langchain.com/docs/integrations/chat/litellm"
    icon = "🚄"

    inputs = [
        MessageInput(name="input_value", display_name="Input"),
        StrInput(
            name="api_base",
            display_name="API Base URL",
            required=False,
            advanced=False,
            info="LiteLLM proxy URL. Example: http://localhost:4000",
        ),
        SecretStrInput(
            name="api_key",
            display_name="API Key",
            advanced=False,
            required=False,
        ),
        DropdownInput(
            name="model",
            display_name="Models",
            options=[""],
            required=True,
            # dynamic=True,
            info="Select a model",
            refresh_button=True,
            real_time_refresh=True,
        ),
        FloatInput(
            name="temperature",
            display_name="Temperature",
            advanced=False,
            required=False,
            value=0.7,
        ),
        DictInput(
            name="kwargs",
            display_name="Kwargs",
            advanced=True,
            required=False,
            is_list=True,
            value={},
        ),
        DictInput(
            name="model_kwargs",
            display_name="Model kwargs",
            advanced=True,
            required=False,
            is_list=True,
            value={},
        ),
        FloatInput(name="top_p", display_name="Top p", advanced=True, required=False, value=0.5),
        IntInput(name="top_k", display_name="Top k", advanced=True, required=False, value=35),
        IntInput(
            name="n",
            display_name="N",
            advanced=True,
            required=False,
            info="Number of chat completions to generate for each prompt. "
            "Note that the API may not return the full n completions if duplicates are generated.",
            value=1,
        ),
        IntInput(
            name="max_tokens",
            display_name="Max tokens",
            advanced=False,
            value=256,
            info="The maximum number of tokens to generate for each chat completion.",
        ),
        IntInput(
            name="max_retries",
            display_name="Max retries",
            advanced=True,
            required=False,
            value=6,
        ),
        BoolInput(
            name="verbose",
            display_name="Verbose",
            advanced=True,
            required=False,
            value=False,
        ),
        BoolInput(
            name="stream",
            display_name="Stream",
            info=STREAM_INFO_TEXT,
            advanced=True,
        ),
        StrInput(
            name="system_message",
            display_name="System Message",
            info="System message to pass to the model.",
            advanced=True,
        ),
    ]

    def build_model(self) -> LanguageModel:  # type: ignore[type-var]
        try:
            import litellm

            litellm.drop_params = True
            litellm.set_verbose = self.verbose
        except ImportError as e:
            msg = "Could not import litellm python package. Please install it with `pip install litellm`"
            raise ChatLiteLLMException(msg) from e
        # Remove empty keys
        if "" in self.kwargs:
            del self.kwargs[""]
        if "" in self.model_kwargs:
            del self.model_kwargs[""]
        if "api_base" not in self.kwargs:
            msg = "Missing api_base on kwargs"
            raise ValueError(msg)
        if "api_version" not in self.model_kwargs:
            msg = "Missing api_version on model_kwargs"
            raise ValueError(msg)
        output = ChatLiteLLM(
            model=f"{self.provider.lower()}/{self.model}",
            client=None,
            streaming=self.stream,
            temperature=self.temperature,
            model_kwargs=self.model_kwargs if self.model_kwargs is not None else {},
            top_p=self.top_p,
            top_k=self.top_k,
            n=self.n,
            max_tokens=self.max_tokens,
            max_retries=self.max_retries,
            **self.kwargs,
        )
        output.client.api_key = self.api_key

        return output
        
    def update_build_config(self, build_config, field_value, field_name = None):
        # return super().update_build_config(build_config, field_value, field_name)
        import requests
        if field_name == "model":
            url = f"{self.api_base.rstrip('/')}/models"
            headers = {
                "accept": "application/json",
                "x-litellm-api-key": self.api_key
            }
            params = {
                "return_wildcard_routes": "false",
                "include_model_access_groups": "false"
            }
            response = requests.get(url, headers=headers, params=params, timeout=5)
            response.raise_for_status()

            models_data = response.json()
            model_list =  [model["id"] for model in models_data.get("data", [])]
            
            # collections = [collection.name for collection in 
            build_config["model"]["options"] = model_list
            build_config["model"]["value"] = model_list[0]
        return build_config